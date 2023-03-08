import numpy as np


def s_lengths(sequence_info: list) -> list:
    # TODO: Naive implementation
    length_list = []
    for element in sequence_info:
        if len(element["attrs"]["symbol"]) not in length_list:
            length_list.append(len(element["attrs"]["symbol"]))
    return length_list


def get_tau(t: float) -> int:
    return int(t - 1) if int(t) == t else int(t)


def get_s_at_length(sequence_info: list, length: int) -> list:
    s_list = []
    for element in sequence_info:
        if len(element["attrs"]["symbol"]) == length:
            s_list.append(element)
    return s_list


def compute_links(tree_data: dict) -> list:
    """Compute the link between nodes with nodes' symbol information

    Parameters
    ----------
    tree_data : dict
        Node dictionary, contains at least "symbol" and "id" information

    Returns
    -------
    list
        List of links in dictionary with keys: source, target

    """
    links_info = []
    sorted_tree = sorted(tree_data["nodes"], key=lambda x: x["symbol"])
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


def compute_coordinates(symbol_sequence: list, dim_space: int) -> np.ndarray:
    """Compute the coordinates for the given symbol sequence.

    Parameters
    ----------
    symbol_sequence : list
        List of ints representing the symbol sequence

    Returns
    -------
    np.ndarray
        The coordinates of the given symbol sequence, each element representing value in corresponding dimension
    """
    coordinates = np.zeros(dim_space, dtype="float64")
    # The origin in the x coordinates is an empty sequence.
    # The index in Python start from 0.
    # In the paper we start it from 1...
    for index, symbol in enumerate(symbol_sequence):
        index += 1  # The math index starts from 1
        if abs(symbol) > dim_space:
            raise ValueError(
                f"Dimension cannot be greater than axis. Got dimension: {dim_space}, axis: {symbol}"
            )
        if symbol != 0:
            movement_length = np.sign(symbol) * 2.0 / (4.0**index)
            x = abs(symbol) - 1  # the 1st axis is x0 internally
            coordinates[x] += movement_length
    return coordinates


def compute_intercept():
    # TODO: Confirm if this can be computed with per-dimension.
    # The diamond should be in the domain, what happen to the diamond at higher dim?
    pass


def compute_distance(
    symbol_sequence: list[int],
    solution_coordinates: np.ndarray,
    dim_space: int,
    diagonal_length: float,
):
    center_coordinates = compute_coordinates(
        symbol_sequence=symbol_sequence, dim_space=dim_space
    )
    print(center_coordinates)
    print(solution_coordinates - center_coordinates)


if __name__ == "__main__":
    test_sequence = [1, 2, 1]
    test_solution_coordinates = np.array([1.5, 1.5])
    compute_distance(
        symbol_sequence=test_sequence,
        solution_coordinates=test_solution_coordinates,
        dim_space=2,
        diagonal_length=5,
    )
