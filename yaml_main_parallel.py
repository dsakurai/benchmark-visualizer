import argparse
import math
import multiprocessing
import typing
from enum import Enum
from multiprocessing import Pool
from pathlib import Path

import yaml
from jmetal.algorithm.multiobjective import NSGAII, MOEAD, OMOPSO, IBEA
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
from jmetal.util.termination_criterion import StoppingByTime, StoppingByEvaluations
from tqdm import tqdm

from custom_benchmark_problems.diamon_problem.apis.jmetal import Diamond
from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree
from utils.data_structures import ExperimentSettings
from utils.parallel_utils import print_err
from utils.tracking import MlflowTracker


class Algorithms(Enum):
    gde3 = "GDE3"
    nsgaii = "NSGAII"
    ibea = "IBEA"
    moead = "MOEAD"
    omopso = "OMOPSO"


def gde3(**kwargs):
    parameters = kwargs["parameters"]
    population_size = parameters["population_size"]
    cr = parameters["cr"]
    f = parameters["f"]

    stopping_criterion = kwargs["termination_criterion"]
    if stopping_criterion["criterion_name"] == "StoppingByTime":
        termination_criterion = StoppingByTime(
            stopping_criterion["termination_parameter"]
        )
    elif stopping_criterion["criterion_name"] == "StoppingByEvaluations":
        termination_criterion = StoppingByEvaluations(
            stopping_criterion["termination_parameter"]
        )
    else:
        raise NotImplementedError("Termination criterion not supported")

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
    stopping_criterion = kwargs["termination_criterion"]
    if stopping_criterion["criterion_name"] == "StoppingByTime":
        termination_criterion = StoppingByTime(
            stopping_criterion["termination_parameter"]
        )
    elif stopping_criterion["criterion_name"] == "StoppingByEvaluations":
        termination_criterion = StoppingByEvaluations(
            stopping_criterion["termination_parameter"]
        )
    else:
        raise NotImplementedError("Termination criterion not supported")

    return NSGAII(
        problem=kwargs["problem"],
        population_size=population_size,
        offspring_population_size=offspring_population_size,
        mutation=mutation,
        crossover=crossover,
        termination_criterion=termination_criterion,
    )


def ibea(**kwargs):
    parameters = kwargs["parameters"]
    kappa = parameters["kappa"]
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
    stopping_criterion = kwargs["termination_criterion"]
    if stopping_criterion["criterion_name"] == "StoppingByTime":
        termination_criterion = StoppingByTime(
            stopping_criterion["termination_parameter"]
        )
    elif stopping_criterion["criterion_name"] == "StoppingByEvaluations":
        termination_criterion = StoppingByEvaluations(
            stopping_criterion["termination_parameter"]
        )
    else:
        raise NotImplementedError("Termination criterion not supported")

    return IBEA(
        problem=kwargs["problem"],
        kappa=kappa,
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
    stopping_criterion = kwargs["termination_criterion"]
    if stopping_criterion["criterion_name"] == "StoppingByTime":
        termination_criterion = StoppingByTime(
            stopping_criterion["termination_parameter"]
        )
    elif stopping_criterion["criterion_name"] == "StoppingByEvaluations":
        termination_criterion = StoppingByEvaluations(
            stopping_criterion["termination_parameter"]
        )
    else:
        raise NotImplementedError("Termination criterion not supported")

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
    stopping_criterion = kwargs["termination_criterion"]
    if stopping_criterion["criterion_name"] == "StoppingByTime":
        termination_criterion = StoppingByTime(
            stopping_criterion["termination_parameter"]
        )
    elif stopping_criterion["criterion_name"] == "StoppingByEvaluations":
        termination_criterion = StoppingByEvaluations(
            stopping_criterion["termination_parameter"]
        )
    else:
        raise NotImplementedError("Termination criterion not supported")

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


def run_experiment(exp_config: ExperimentSettings, opts):
    with MlflowTracker(
        run_name=exp_config.experiment_name, experiment_config=exp_config
    ) as tracker:
        tree = Tree(dim_space=exp_config.dimension)
        tree.from_json(exp_config.tree_file)
        problem = Diamond(
            dim_space=exp_config.dimension,
            sequence_info=tree.to_sequence(),
            enable_tracking=opts.disable_tracking,
            tracker=tracker,
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
                pass
                # print(solution)

        # print("**********************")

        fronts = get_non_dominated_solutions(solutions)
        for front in fronts:
            pass
            # print(front)


def yaml_main(opts):
    exps_config = load_experiment_settings(file_path=Path(opts.file))
    cpus = multiprocessing.cpu_count()
    pool = Pool(processes=cpus)
    pbar = tqdm(total=len(exps_config))
    pbar.set_description("Experiment Progress")

    def pbar_update(*args):
        pbar.update()

    for exp_config in exps_config:
        if opts.exp_name:
            exp_config.experiment_name = opts.exp_name
        pool.apply_async(
            run_experiment,
            args=(
                exp_config,
                opts,
            ),
            error_callback=print_err,
            callback=pbar_update,
        )
    pool.close()
    pool.join()
    pbar.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Specify the input YAML experiment file",
        required=True,
    )
    parser.add_argument(
        "--exp_name", type=str, help="Set experiment name, not required"
    )
    parser.add_argument("--disable_tracking", action="store_false")
    yaml_main(parser.parse_args())
