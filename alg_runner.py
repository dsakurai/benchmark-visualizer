from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.util.termination_criterion import StoppingByEvaluations


class AlgRunner:
    def __init__(self):
        self.algorithm = None
        self.problem = None
        self.max_evaluations = 25000

    def load_algorithm(self):
        self.algorithm = GDE3(
            problem=self.problem,
            population_size=100,
            cr=0.5,
            f=0.5,
            termination_criterion=StoppingByEvaluations(self.max_evaluations),
        )

    def run_algorithm(self):
        if self.algorithm is None or self.problem is None:
            raise ValueError("Algorithm or problem not specified")
        self.algorithm.run()
