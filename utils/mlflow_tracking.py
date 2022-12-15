import os

import mlflow
import urllib3
from urllib3.exceptions import InsecureRequestWarning


class Tracking:
    def __init__(
        self,
        experiment_name: str,
        tracking_uri: str = "http://xomics.cc.kyushu-u.ac.jp:5000",
    ):
        os.environ["MLFLOW_TRACKING_INSECURE_TLS"] = "true"
        urllib3.disable_warnings(InsecureRequestWarning)
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        mlflow.start_run(
            run_id=None, experiment_id=None, run_name=None, tags=None, description=None
        )
        self.step = 0
        self.dict_keys = None

    def log_step(
        self,
        variables: list,
        objectives: list,
        constrains: list = None,
        log_interval: int = 100,
    ):
        if self.step % log_interval == 0:
            if constrains:
                raise NotImplementedError("Constrains logging is not available yet")
            if not self.dict_keys:
                self.create_dict_keys(variables=variables, objectives=objectives)
            metrics = dict(zip(self.dict_keys, variables + objectives))
            mlflow.log_metrics(metrics=metrics, step=self.step)
            print(self.step)
        self.step += 1

    def create_dict_keys(
        self, variables: list, objectives: list, constrains: list = None
    ) -> None:
        variable_header = [f"x{x + 1}" for x in range(len(variables) - 1)]
        variable_header.insert(0, "t")
        objective_header = [f"y{x + 1}" for x in range(len(objectives))]
        self.dict_keys = variable_header + objective_header
