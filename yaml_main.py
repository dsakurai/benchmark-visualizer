import argparse
import math
import typing
from enum import Enum
from pathlib import Path
from typing import NamedTuple, Dict, Any

import yaml
from jmetal.algorithm.multiobjective import NSGAII, MOEAD, OMOPSO
from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.operator import (
    PolynomialMutation,
    SBXCrossover,
    DifferentialEvolutionCrossover,
    UniformMutation,
)
from jmetal.operator.mutation import NonUniformMutation
from jmetal.util.aggregative_function import Tschebycheff
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByTime

from custom_benchmark_problems.diamon_problem.apis.jmetal import Diamond
from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


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
    termination_criterion = StoppingByTime(
        kwargs["termination_criterion"]["termination_parameter"]
    )

    return GDE3(
        problem=kwargs["problem"],
        population_size=population_size,
        cr=cr,
        f=f,
        termination_criterion=termination_criterion,
    )


def nsgaii(**kwargs):
    parameters = kwargs["parameters"]
    population_size = parameters["population_size"]
    offspring_population_size = parameters["offspring_population_size"]
    mutation_parameters = parameters["mutation"]
    crossover_parameters = parameters["crossover"]
    if mutation_parameters["probability"] == "n_variables":
        probability = 1 / kwargs["exp_config"].dimension
    elif type(mutation_parameters["probability"]) is float:
        probability = mutation_parameters["probability"]
    else:
        raise NotImplementedError("Invalid mutation probability")
    mutation = PolynomialMutation(
        probability=probability,
        distribution_index=mutation_parameters["distribution_index"],
    )
    crossover = SBXCrossover(
        probability=crossover_parameters["probability"],
        distribution_index=crossover_parameters["distribution_index"],
    )
    termination_criterion = StoppingByTime(
        kwargs["termination_criterion"]["termination_parameter"]
    )

    return NSGAII(
        problem=kwargs["problem"],
        population_size=population_size,
        offspring_population_size=offspring_population_size,
        mutation=mutation,
        crossover=crossover,
        termination_criterion=termination_criterion,
    )


def moead(**kwargs):
    parameters = kwargs["parameters"]
    population_size = parameters["population_size"]
    mutation_parameters = parameters["mutation"]
    crossover_parameters = parameters["crossover"]
    if mutation_parameters["probability"] == "n_variables":
        probability = 1 / (kwargs["exp_config"].dimension + 1)
    elif type(mutation_parameters["probability"]) is float:
        probability = mutation_parameters["probability"]
    else:
        raise NotImplementedError("Invalid mutation probability")
    mutation = PolynomialMutation(
        probability=probability,
        distribution_index=mutation_parameters["distribution_index"],
    )
    crossover = DifferentialEvolutionCrossover(
        CR=crossover_parameters["CR"],
        F=crossover_parameters["F"],
        K=crossover_parameters["K"],
    )
    aggregative_function = Tschebycheff(dimension=kwargs["exp_config"].dimension + 1)
    termination_criterion = StoppingByTime(
        kwargs["termination_criterion"]["termination_parameter"]
    )

    return MOEAD(
        problem=kwargs["problem"],
        population_size=population_size,
        mutation=mutation,
        crossover=crossover,
        aggregative_function=aggregative_function,
        neighbor_size=parameters["neighbor_size"],
        neighbourhood_selection_probability=parameters[
            "neighbourhood_selection_probability"
        ],
        max_number_of_replaced_solutions=parameters["max_number_of_replaced_solutions"],
        weight_files_path=parameters["weight_files_path"],
        termination_criterion=termination_criterion,
    )


def omopso(**kwargs):
    parameters = kwargs["parameters"]
    swarm_size = parameters["swarm_size"]
    epsilon = parameters["epsilon"]

    uniform_mutation_parameters = parameters["uniform_mutation"]
    if uniform_mutation_parameters["probability"] == "n_variables":
        uniform_probability = 1 / (kwargs["exp_config"].dimension + 1)
    elif type(uniform_mutation_parameters["probability"]) is float:
        uniform_probability = uniform_mutation_parameters["probability"]
    else:
        raise NotImplementedError("Invalid mutation probability")
    uniform_mutation = UniformMutation(
        probability=uniform_probability,
        perturbation=uniform_mutation_parameters["perturbation"],
    )

    non_uniform_mutation_parameters = parameters["non_uniform_mutation"]
    if uniform_mutation_parameters["probability"] == "n_variables":
        non_uniform_probability = 1 / (kwargs["exp_config"].dimension + 1)
    elif type(uniform_mutation_parameters["probability"]) is float:
        non_uniform_probability = non_uniform_mutation_parameters["probability"]
    else:
        raise NotImplementedError("Invalid mutation probability")
    non_uniform_mutation = NonUniformMutation(
        probability=non_uniform_probability,
        perturbation=non_uniform_mutation_parameters["perturbation"],
        max_iterations=int(25000 / 100),
    )

    leaders = CrowdingDistanceArchive(
        maximum_size=parameters["leaders"]["maximum_size"]
    )
    termination_criterion = StoppingByTime(
        kwargs["termination_criterion"]["termination_parameter"]
    )

    return OMOPSO(
        problem=kwargs["problem"],
        swarm_size=swarm_size,
        epsilon=epsilon,
        uniform_mutation=uniform_mutation,
        non_uniform_mutation=non_uniform_mutation,
        leaders=leaders,
        termination_criterion=termination_criterion,
    )


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
        algorithm = globals()[Algorithms(exp_config.algorithm).name](
            problem=problem,
            exp_config=exp_config,
            parameters=exp_config.algorithm_parameters,
            termination_criterion=exp_config.termination_criterion,
        )
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
