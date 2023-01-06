from custom_benchmark_problems.diamon_problem.core.evaluation import BMP


def validate_tree_minima(sequence_data: list, dim_space: int):
    print("Validating ...")
    sorted_sequence = parse_node_info(sequence_data)
    t = 15
    while sorted_sequence:
        current_node = sorted_sequence.pop()
        bmp = BMP(sequence_info=sorted_sequence, dim_space=dim_space)
        minimal_coordinates = bmp.compute_coordinates(current_node["attrs"]["symbol"])
        computed_minimal = bmp.evaluate()


def compute_minimal():
    pass


def get_minimal_coordinates():
    pass


def parse_node_info(sequence_data: list) -> list:
    sequence_data = sorted(sequence_data, key=lambda node: len(node["attrs"]["symbol"]))
    return sequence_data
