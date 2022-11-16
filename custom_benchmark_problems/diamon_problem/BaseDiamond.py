import math

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


# TODO: Specify an official name
class Diamond(FloatProblem):
    def __init__(self, construction_tree: Tree, dim_space: int):
        super(Diamond, self).__init__()
        self.number_of_variables = dim_space + 1
        self.number_of_objectives = 2
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["f(x)"]
        # Lower bound for normal variables
        self.lower_bound = dim_space * [-2.0]
        # Lower bound for time
        self.lower_bound.append(-1.0)
        # Upper bound for normal variables
        self.upper_bound = dim_space * [2.0]
        # TODO: Check if inf is allowed for upper bound
        # Upper bound for time
        self.upper_bound.append(math.inf)
        self.tree = construction_tree

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        # TODO: Verify how to optimize time
        solution.objectives[0] = self.tree.value_at(
            xt=solution.variables, tree=self.tree
        )
        return solution

    def get_name(self) -> str:
        return "diamond"
