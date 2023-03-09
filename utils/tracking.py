import argparse
import datetime
import os
import sys
import traceback
import typing

import mlflow
import numpy as np
import pandas as pd
from mlflow.tracking import MlflowClient

from config import mlflow_tracking_uri, data_dir
from utils.data_structures import ExperimentSettings
from utils.log import Logger

ArgParserFunc = typing.Callable[
    [typing.Optional[argparse.ArgumentParser]], argparse.Namespace
]


class MlflowTracker:
    def __init__(self, run_name: str, experiment_config: ExperimentSettings):
        self.run_name = run_name
        self.experiment_config = experiment_config
        self.step = 0
        self.headers = None
        self.step_metrics = []

    def __enter__(self):
        try:
            client = MlflowClient()
            mlflow.set_tracking_uri(mlflow_tracking_uri)
            experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME")

            if experiment_name:
                mlflow.set_experiment(experiment_name)
            else:
                Logger().debug.info(
                    "Experiment not found, using default ... "
                    "(Set MLFLOW_EXPERIMENT_NAME in environment variable to change this behavior)"
                )
            mlflow.start_run(run_name=self.run_name)
            artifact_dir = data_dir / "MLproject"
            os.makedirs(artifact_dir, exist_ok=True)
            mlflow.log_artifact(artifact_dir)
            mlflow.log_params(self.experiment_config._asdict())

            return self
        except Exception as e:
            self.__exit__(*sys.exc_info())
            raise

    def log_step(
        self,
        variables: list,
        objectives: list,
        eval_node_id: int,
        diagonal_length: float,
        org_objectives: list,
        constrains: list = None,
    ):
        if constrains:
            raise NotImplementedError("Constrains logging is not available yet")
        if not self.headers:
            self.create_headers(variables=variables, objectives=objectives)

        self.step_metrics.append(
            variables
            + objectives
            + [eval_node_id, diagonal_length, self.step]
            + org_objectives
        )
        self.step += 1

    def create_headers(
        self, variables: list, objectives: list, constrains: list = None
    ) -> None:
        variable_header = [f"x{x + 1}" for x in range(len(variables) - 1)]
        variable_header.insert(0, "t")
        objective_header = [f"y{x + 1}" for x in range(len(objectives))]
        self.headers = (
            variable_header
            + objective_header
            + ["eval_node_id", "diagonal_length", "step", "t_org", "y_org"]
        )

    def send_data(self):
        self.step_metrics = np.array(self.step_metrics)
        step_metrics_df = pd.DataFrame(self.step_metrics, columns=self.headers)
        algorithm = self.experiment_config.algorithm
        tree_file = self.experiment_config.tree_file.split(".")[0]
        dimension = self.experiment_config.dimension
        termination_criterion = self.experiment_config.termination_criterion[
            "criterion_name"
        ]
        file_name = (
            f"{algorithm}_"
            f"{tree_file.split('/')[1]}_"
            f"{dimension}_"
            f"{termination_criterion}_"
            f"{datetime.datetime.now().isoformat().replace(':', '-')}.csv"
        )
        print(file_name)
        step_metrics_df.to_csv(file_name)
        mlflow.log_artifact(local_path=file_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # executed when an error occurred
        if exc_type is not None:
            # Send error logs to Mlflow server
            traceback.print_exc(file=open("errlog.txt", "w"))
            mlflow.log_artifact("errlog.txt")
        self.send_data()
        sys.stdout.flush()
        sys.stderr.flush()
        mlflow.end_run()
