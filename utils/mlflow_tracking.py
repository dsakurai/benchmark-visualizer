import atexit
import datetime
import os
from typing import Optional

import mlflow
import numpy as np
import pandas as pd
import urllib3
from urllib3.exceptions import InsecureRequestWarning


class Tracking:
    #
    # TODO: INTEGRATE THIS FOR TRACK SERVER CHECKING, URGENT
    # if tracking is True:  # Check if the server is available
    #     class BadCode(Exception):
    #         def __init__(self, message):
    #             BadCode(message)
    #
    #     timeout = 5
    #     try:
    #         import urllib.request
    #         code = urllib.request.urlopen(mlflow_url, timeout=timeout).getcode()
    #         if code != 200: raise BadCode("Website returned code {}".format(code))
    #     except BadCode:
    #         raise
    #     except:
    #         print(
    #             "Error: mlflow server error (with {} sec timeout). First, make sure you have access to {} by opening the URL with a browser.".format(
    #                 timeout, mlflow_url))
    #         raise
    def __init__(
        self,
        experiment_name: str,
        tracking_uri: str,
        tracking_parameters: Optional[dict] = None,
    ):
        if mlflow.active_run():
            mlflow.end_run()
        os.environ["MLFLOW_TRACKING_INSECURE_TLS"] = "true"
        urllib3.disable_warnings(InsecureRequestWarning)
        self.experiment_name = experiment_name
        # mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        if tracking_parameters:
            mlflow.start_run(
                run_id=tracking_parameters.get("run_id"),
                experiment_id=tracking_parameters.get("experiment_id"),
                run_name=tracking_parameters.get("run_name"),
                tags=tracking_parameters.get("tags"),
                description=tracking_parameters.get("description"),
            )
        else:
            mlflow.start_run()
        self.step = 0
        self.headers = None
        self.step_metrics = []
        atexit.register(self.send_data)

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
        file_name = f"{self.experiment_name}_{datetime.datetime.now().isoformat().replace(':', '-')}.csv"
        step_metrics_df.to_csv(file_name)
        mlflow.log_artifact(local_path=file_name)
