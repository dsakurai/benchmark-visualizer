import os

import mlflow
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import numpy as np
import datetime

class Tracking:
    def __init__(
        self,
        experiment_name: str,
        tracking_uri: str = "http://xomics.cc.kyushu-u.ac.jp:5000",
    ):
        os.environ["MLFLOW_TRACKING_INSECURE_TLS"] = "true"
        urllib3.disable_warnings(InsecureRequestWarning)
        self.experiment_name = experiment_name
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        mlflow.start_run(
            run_id=None, experiment_id=None, run_name=None, tags=None, description=None
        )
        self.step = 0
        self.dict_keys = None
        self.step_metrics = []

    def log_step(
        self,
        variables: list,
        objectives: list,
        constrains: list = None,
    ):
        if constrains:
            raise NotImplementedError("Constrains logging is not available yet")
        if not self.dict_keys:
            self.create_dict_keys(variables=variables, objectives=objectives)

        self.step_metrics.append(variables + objectives + [self.step])
        self.step += 1

    def create_dict_keys(
        self, variables: list, objectives: list, constrains: list = None
    ) -> None:
        variable_header = [f"x{x + 1}" for x in range(len(variables) - 1)]
        variable_header.insert(0, "t")
        objective_header = [f"y{x + 1}" for x in range(len(objectives))]
        self.dict_keys = variable_header + objective_header

    def send_data(self):
        self.step_metrics = np.array(self.step_metrics)
        file_name = f"{self.experiment_name}_{datetime.datetime.now().isoformat()}.npz"
        self.step_metrics.dump(file_name)
        mlflow.log_artifact(local_path=file_name)
