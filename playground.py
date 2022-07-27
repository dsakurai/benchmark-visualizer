import math

from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.problem import ZDT1
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations

from custom_benchmark_problems.single_objective import HolderTable
from core.status_logger import StatusLogger

logger = StatusLogger()
problem = ZDT1()
problem2 = HolderTable(logger=logger)


max_evaluations = 25000

algorithm = GDE3(
    problem=problem2,
    population_size=100,
    cr=0.5,
    f=0.5,
    termination_criterion=StoppingByEvaluations(max_evaluations),
)

algorithm.run()
solutions = algorithm.get_result()
logger.plot_solution()
# logger.plot_variable()
for solution in solutions:
    x_1 = solution.variables[0]
    x_2 = solution.variables[1]
    y = abs(1 - math.sqrt(x_1**2 + x_2**2) / math.pi)
    y = -abs(math.sin(x_1) * math.cos(x_2) * math.exp(y))
    if y - solution.objectives[0] > 0:
        print(solution)

fronts = get_non_dominated_solutions(solutions)
for front in fronts:
    print(front)
