import math
from typing import Optional

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from utils import mlflow_tracking


class HolderTable(FloatProblem):
    def __init__(self, number_of_variables: int = 2, logger: Optional = None):
        super(HolderTable, self).__init__()
        self.number_of_variables = number_of_variables
        self.number_of_objectives = 1
        self.number_of_constraints = 0
        if logger:
            self.logger = logger

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["f(x)"]

        self.lower_bound = self.number_of_variables * [-10.0]
        self.upper_bound = self.number_of_variables * [10.0]

        self.tracking = mlflow_tracking.Tracking(experiment_name="test_run")

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x_1 = solution.variables[0]
        x_2 = solution.variables[1]

        y = abs(1 - math.sqrt(x_1**2 + x_2**2) / math.pi)
        y = -abs(math.sin(x_1) * math.cos(x_2) * math.exp(y))

        solution.objectives[0] = y
        self.tracking.log_step(variables=solution.variables,objectives=solution.objectives)
        return solution

    def get_name(self) -> str:
        return "HolderTable"


# ZDT1:
"""
g(x) = 1 + 9 (sigma x_i) / (n - 1)
f_1(x) = x_1
h(x) = g(x)[1-(x_1/g(x))^0.5]
x -> [0,1]
"""
# Holder table:
"""
-|sin(x_1)cos(x_2)exp(|1-(x_1^2+x_2^2)^0.5)/pi|)|
x -> [-10,10]
"""
