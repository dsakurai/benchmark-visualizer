import datetime
import os
from pathlib import Path

import mlflow
import numpy as np
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from typing import Optional
import atexit
import os


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
        self.dict_keys = None
        self.step_metrics = []
        atexit.register(self.send_data)

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
        # TODO: Use CSV format
        self.step_metrics = np.array(self.step_metrics)
        file_name = f"{self.experiment_name}_{datetime.datetime.now().isoformat().replace(':','-')}.npz"
        self.step_metrics.dump(file_name)
        mlflow.log_artifact(local_path=file_name)
