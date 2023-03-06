import argparse
import math
from enum import Enum
from pathlib import Path

from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.operator import SBXCrossover, PolynomialMutation

from custom_benchmark_problems.diamon_problem.apis.jmetal import Diamond
from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree

import typing
from typing import NamedTuple, Dict, Any
import yaml


class ExperimentSettings(NamedTuple):
    experiment_name: str
    tree_file: str
    dimension: int
    algorithm: str
    algorithm_parameters: Dict[str, Any]
    termination_criterion: Dict[str, Any]


class Algorithms(Enum):
    gde3 = "GDE3"
    nsgaii = "NSGAII"
    moead = "MOEAD"
    omopso = "OMOPSO"


def gde3(**kwargs):
    parameters = kwargs["parameters"]
    population_size = parameters["population_size"]
    cr = parameters["cr"]
    f = parameters["f"]

    return GDE3(problem=kwargs["problem"],
                population_size=100,
                cr=0.5,
                f=0.5,
                termination_criterion=StoppingByEvaluations(max_evaluations),
                )


def nsgaii(**kwargs):
    print("nsgaii")
    pass


def moead(**kwargs):
    pass


def omopso(**kwargs):
    pass


def load_experiment_settings(file_path: Path) -> typing.List[ExperimentSettings]:
    with file_path.open() as file:
        settings = yaml.safe_load(file)
    return [ExperimentSettings(**setting) for setting in settings]


def yaml_main(opts):
    exps_config = load_experiment_settings(file_path=Path(opts.file))
    tracking_parameters = {
        "run_id": None,
        "experiment_id": None,
        "run_name": "First Run",
        "tags": {"test_version": "0.0.1"},
        "description": "Tracking parameters are not required, but is a Nice-to-have."
                       " You could fill some of these parameters for identification",
    }
    for exp_config in exps_config:
        tree = Tree(dim_space=exp_config.dimension)
        tree.from_json(exp_config.tree_file)
        problem = Diamond(
            dim_space=exp_config.dimension,
            sequence_info=tree.to_sequence(),
            enable_tracking=opts.disable_tracking,
            tracking_uri="http://xomics.cc.kyushu-u.ac.jp:5000",
            experiment_name="test_runx",
            tracking_parameters=tracking_parameters,
        )
        algorithm = globals()[Algorithms(exp_config.algorithm).name](problem=problem,
                                                                     parameters=exp_config.algorithm_parameters,
                                                                     termination_criterion=exp_config.termination_criterion)


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
        tracking_uri="http://xomics.cc.kyushu-u.ac.jp:5000",
        experiment_name="test_runx",
        tracking_parameters=tracking_parameters,
    )

    # GDE3 Settings
    max_evaluations = 25000

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
        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        crossover=SBXCrossover(probability=1.0, distribution_index=20),
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
    yaml_main(parser.parse_args())
