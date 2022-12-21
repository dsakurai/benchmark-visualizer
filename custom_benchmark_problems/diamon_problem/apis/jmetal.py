from typing import Optional

import mlflow
import numpy as np
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

from custom_benchmark_problems.diamon_problem.core import evaluation
from utils import mlflow_tracking


class Diamond(FloatProblem):
    def __init__(
        self,
        dim_space: int,
        sequence_info: list[dict],
        enable_tracking: bool = False,
        experiment_name: Optional[str] = None,
        tracking_uri: Optional[str] = None,
        tracking_parameters: Optional[dict] = None,
        algorithm_parameters: Optional[dict] = None,
    ):
        super(Diamond, self).__init__()
        self.number_of_variables = dim_space + 1
        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.problem = evaluation.BMP(sequence_info=sequence_info, dim_space=dim_space)

        self.obj_directions = [self.MINIMIZE]
        self.obj_lables = ["f(x)"]
        # TODO: Known issue here, cause huge problem
        # Exit code -1073741571 (0xC00000FD)
        self.lower_bound = dim_space * [-1.0]
        self.lower_bound.insert(0, 0.0)
        self.upper_bound = dim_space * [1.0]
        self.upper_bound.insert(0, 10.0)
        self.enable_tracking = enable_tracking
        if enable_tracking:
            assert experiment_name is not None, "Experiment name not set"
            assert tracking_uri is not None, "Tracking URI not set"
            self.tracking = mlflow_tracking.Tracking(
                experiment_name=experiment_name,
                tracking_uri=tracking_uri,
                tracking_parameters=tracking_parameters,
            )
            self.tracking_list = []
            mlflow.log_params({"sequence": sequence_info})
            if algorithm_parameters:
                mlflow.log_params(algorithm_parameters)

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        eval_results = self.problem.evaluate(
            solution_variables=np.array(solution.variables, dtype="float64")
        )
        solution.objectives[0] = eval_results[0]
        solution.objectives[1] = eval_results[1]
        if self.enable_tracking:
            self.tracking.log_step(
                variables=solution.variables, objectives=solution.objectives
            )
        return solution

    def get_name(self) -> str:
        return "diamond"
