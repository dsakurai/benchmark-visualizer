import argparse
import math

from jmetal.algorithm.multiobjective import IBEA
from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations

from custom_benchmark_problems.diamon_problem.apis.jmetal import Diamond
from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


def cli_main(opts):
    # Construct the tree from file
    tree = Tree(dim_space=opts.dim)

    tree.from_json(opts.file)

    tracking_parameters = {
        "run_id": None,
        "experiment_id": None,
        "run_name": "First Run",
        "tags": {"test_version": "0.0.1"},
        "description": "Tracking parameters are not required, but is a Nice-to-have."
                       " You could fill some of these parameters for identification",
    }

    # Problem construction, again, tracking_parameters are not required
    problem = Diamond(
        dim_space=opts.dim,
        sequence_info=tree.to_sequence(),
        enable_tracking=opts.disable_tracking,
    )

    # GDE3 Settings
    max_evaluations = 2500

    algorithm = GDE3(
        problem=problem,
        population_size=100,
        cr=0.5,
        f=0.5,
        termination_criterion=StoppingByEvaluations(max_evaluations),
    )

    algorithm = NSGAII(
        problem=problem,
        population_size=100,
        offspring_population_size=100,
        mutation=PolynomialMutation(
            probability=1.0 / problem.number_of_variables, distribution_index=20
        ),
        crossover=SBXCrossover(probability=1.0, distribution_index=20),
        termination_criterion=StoppingByEvaluations(max_evaluations),
    )

    algorithm = IBEA(
        problem=problem,
        kappa=1.0,
        population_size=100,
        offspring_population_size=100,
        mutation=PolynomialMutation(
            probability=1.0 / problem.number_of_variables, distribution_index=20
        ),
        crossover=SBXCrossover(probability=1.0, distribution_index=20),
        termination_criterion=StoppingByEvaluations(max_evaluations),
    )

    # Run GDE3
    algorithm.run()

    # Get solutions
    solutions = algorithm.get_result()
    # print(solutions)

    # Print the results
    for solution in solutions:
        x_1 = solution.variables[0]
        x_2 = solution.variables[1]
        y = abs(1 - math.sqrt(x_1 ** 2 + x_2 ** 2) / math.pi)
        y = -abs(math.sin(x_1) * math.cos(x_2) * math.exp(y))
        if y - solution.objectives[0] > 0:
            print(solution)

    print("**********************")

    fronts = get_non_dominated_solutions(solutions)
    for front in fronts:
        print(front)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="Specify the input json file", required=True
    )
    parser.add_argument("--dim", type=int, help="Dimension of the problem", default=2)
    parser.add_argument("--disable_tracking", action="store_false")
    cli_main(parser.parse_args())
