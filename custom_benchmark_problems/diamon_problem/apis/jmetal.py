import math

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution


class Diamond(FloatProblem):
    def __init__(self, dim_space: int):
        super(Diamond, self).__init__()
        self.number_of_variables = dim_space + 1
        self.number_of_objectives = 2
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_lables = ["f(x)"]
        self.lower_bound = dim_space * [-math.inf]
        self.lower_bound.append(0.0)
        self.upper_bound = dim_space * [2.0]
        self.upper_bound.append(math.inf)

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        solution.objectives[0] = evaluate()
        pass