import math

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from custom_benchmark_problems.diamon_problem.core import evaluation
from utils import mlflow_tracking
import mlflow


class Diamond(FloatProblem):
    def __init__(self, dim_space: int, sequence_info: list[dict], enable_tracking: bool = False):
        super(Diamond, self).__init__()
        self.number_of_variables = dim_space + 1
        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.problem = evaluation.BMP(sequence_info=sequence_info, dim_space=dim_space)

        self.obj_directions = [self.MINIMIZE]
        self.obj_lables = ["f(x)"]
        self.lower_bound = dim_space * [-math.inf]
        self.lower_bound.append(0.0)
        self.upper_bound = dim_space * [2.0]
        self.upper_bound.append(math.inf)
        if enable_tracking:
            self.tracking = mlflow_tracking.Tracking(experiment_name="test_run")



    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        solution.objectives[0] = None
        self.tracking.log_step()
