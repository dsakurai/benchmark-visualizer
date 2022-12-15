import argparse
import math
from pathlib import Path

from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations

from custom_benchmark_problems.diamon_problem.apis.jmetal import Diamond
from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


def cli_main(opts):
    # Construct the tree from file
    tree = Tree(dim_space=opts.dim)
    base_path = Path(__file__).parent.absolute()
    data_path = base_path / "sample.json"
    tree.from_json(data_path)
    # Problem construction
    problem = Diamond(dim_space=opts.dim, sequence_info=tree.to_sequence())

    # GDE3 Settings
    max_evaluations = 25000
    algorithm = GDE3(
        problem=problem,
        population_size=100,
        cr=0.5,
        f=0.5,
        termination_criterion=StoppingByEvaluations(max_evaluations),
    )

    # Run GDE3
    algorithm.run()

    # Get solutions
    solutions = algorithm.get_result()

    # Print the results
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Specify the input json file",
        default="sample.json",
    )
    parser.add_argument("--dim", type=int, help="Dimension of the problem", default=2)
    cli_main(parser.parse_args())
