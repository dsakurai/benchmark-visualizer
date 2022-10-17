from pathlib import Path

import numpy as np

from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


def compute_links(tree_data: dict) -> list:
    """Compute the link between nodes with nodes' symbol information

    Parameters
    ----------
    tree_data : dict
        Node dictionary, contains at least "symbol" and "id" information

    Returns
    -------
    list
        list of links in dictionary with keys: source, target

    """
    links_info = []
    sorted_tree = sorted(tree_data["nodes"], key=lambda x: x['symbol'])
    sorted_tree.reverse()
    for index, node in enumerate(sorted_tree):
        if node["id"] == 0:
            continue
        previous_node = find_previous_node(node, index, sorted_tree)
        if previous_node:
            links_info.append({"source": previous_node["id"], "target": node["id"]})
        else:
            links_info.append({"source": 0, "target": node["id"]})
    return links_info


def find_previous_node(current_node: dict, index: int, sorted_tree: list) -> dict:
    """Find the previous node in tree

    Parameters
    ----------
    current_node : dict
        Current node information
    index : int
        Current search index in tree
    sorted_tree : list
        Tree information, sorted by the length of "symbol" in reverse order (Longer one goes first)

    Returns
    -------
    dict
        Previous node of the current node

    """
    for i in range(index, len(sorted_tree) - 1):
        if check_sublist(sorted_tree[i + 1]["symbol"], current_node["symbol"]):
            return sorted_tree[i + 1]


def check_sublist(new_list: list, org_list: list) -> bool:
    # TODO: Naive implementation, may need to change
    iter_length = len(new_list) if len(new_list) < len(org_list) else len(org_list)
    for i in range(iter_length):
        if new_list[i] != org_list[i]:
            return False
    return True


def compute_sign(solution_variables: tuple, candidate_coordinates: list) -> np.ndarray:
    solution_variables = np.array(solution_variables)
    candidate_coordinates = np.array(candidate_coordinates)
    assert solution_variables.shape == candidate_coordinates, "Solution dimension and candidates dimension not match"
    differential = solution_variables - candidate_coordinates
    return differential / np.absolute(differential)


def h_i_x(solution_variables: tuple, candidate_coordinates: list, tau: int):
    signs = compute_sign(solution_variables=solution_variables, candidate_coordinates=candidate_coordinates)
    return signs / (4 ** tau)

def compute_coordinates(symbol_sequence: list, dim_space: int) -> list:
    coordinates = [0 for _ in range(dim_space)]
    for index, symbol in enumerate(symbol_sequence):
        if abs(symbol) + 1 > dim_space:
            raise ValueError(f"Dimension cannot be greater than axis. Got dimension: {dim_space}, axis: {symbol}")
        if symbol != 0:
            movement_length = symbol / abs(symbol) / (4 ** (index + 1))
            coordinates[abs(symbol) - 1] += movement_length
        yield coordinates


# TODO: Change this function name
# TODO: Dummy code for iteration simulation
def main():
    ts = 10
    for t in range(ts):
        if t == 0:
            f_t = 0
        else:
            for iteration in range(t):
                pass





if __name__ == "__main__":
    tree = Tree(dim_space=2)
    base_path = Path(__file__).parent.absolute().parents[2]
    data_path = base_path / "sample.json"
    tree.from_json(str(data_path))
    tree.load_edge(compute_links(tree.to_json()))
    print(tree)
    for item in (compute_coordinates([-2, 1, 1, 2, 0, -1], 2)):
        print(item)
    # sequence = tree.read_path(2)
    # tree.evaluate(sequence, [1.0, 2.0])
