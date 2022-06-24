import argparse

from jmetal.algorithm.multiobjective.gde3 import GDE3
from jmetal.util.termination_criterion import StoppingByEvaluations

from core.problem_constructor import ProblemConstructor
from custom_benchmark_problems.multiobjective import Diamond
from utils import file_utils
from utils import graph_utils


def cli_main(opts: argparse.ArgumentParser.parse_args):
    problem_constructor = ProblemConstructor()
    json_tree = file_utils.read_json_tree(opts.file)
    graph = graph_utils.dict2graph(json_tree)
    print(graph)
    problem_tree = problem_constructor.graph_to_problem_tree(
        graph=graph, dim_space=opts.dim
    )
    problem = Diamond(construction_tree=problem_tree, dim_space=opts.dim)
    # algorithm = GDE3(
    #     problem=problem,
    #     population_size=100,
    #     cr=0.5,
    #     f=0.5,
    #     termination_criterion=StoppingByEvaluations(25000),
    # )
    # algorithm.run()
    # solutions = algorithm.get_result()
    # print(solutions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO: Remove default value
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Specify the input json file",
        default="sample.json",
    )
    parser.add_argument("--dim", type=int, help="Dimension of the problem", default=2)
    cli_main(parser.parse_args())
