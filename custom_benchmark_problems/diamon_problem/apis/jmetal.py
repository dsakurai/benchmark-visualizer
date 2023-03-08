from typing import Optional

import mlflow
import numpy as np
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

from custom_benchmark_problems.diamon_problem.core import evaluation
from utils.tracking import MlflowTracker


class Diamond(FloatProblem):
    def __init__(
        self,
        dim_space: int,
        sequence_info: list[dict],
        enable_tracking: bool = False,
        tracker: Optional[MlflowTracker] = None,
    ):
        super(Diamond, self).__init__()
        self.number_of_variables = dim_space + 1
        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.problem = evaluation.BMP(sequence_info=sequence_info, dim_space=dim_space)

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["f(x)"]
        self.lower_bound = dim_space * [-1.0]
        self.lower_bound.insert(0, 0.0)
        self.upper_bound = dim_space * [1.0]
        self.upper_bound.insert(0, self.problem.t_upper_bound())
        self.enable_tracking = enable_tracking
        if enable_tracking:
            self.tracking_list = []
            self.tracker = tracker
            mlflow.log_dict(sequence_info, "sequence.json")

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        eval_results = self.problem.evaluate(
            solution_variables=np.array(solution.variables, dtype="float64")
        )
        solution.objectives[0] = eval_results[0]
        solution.objectives[1] = eval_results[1]
        if self.enable_tracking:
            self.tracker.log_step(
                variables=solution.variables,
                objectives=solution.objectives,
                eval_node_id=eval_results[2],
                diagonal_length=eval_results[3],
                org_objectives=eval_results[4],
            )
        return solution

    def get_name(self) -> str:
        return "diamond"
