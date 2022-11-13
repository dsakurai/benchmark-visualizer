"""
Note: Let's do it this way, compute f(t:int, parameter) = values and t as given value.
Store S and t value pair in dictionary for further usage.
"""

import numpy as np

from algs import *


class BMP:
    def __init__(self, sequence_info: list):
        self.sequence_info = sequence_info
        self.s_lengths = s_lengths(sequence_info)


def evaluate(solution_variables: tuple, sequence_info: list) -> np.ndarray:
    t = solution_variables[-1]
    x = solution_variables[:-1]
    tau = get_tau(t)
    problem = BMP(sequence_info=sequence_info)

    while True:
        if tau in problem.s_lengths:
            pass
        else:
            tau -= 1
        break
    return np.array([])


def process_sequence(sequence: list):
    # TODO: Change naming here, don't want to do this right now
    s_dict = {}
    for item in sequence:
        minima = item["minima"]
        symbol = item["attrs"]["symbol"]
        name = item["name"]
        len_s = len(symbol)
        if len_s in s_dict:
            s_dict[len_s].append((symbol, minima, name))
        else:
            s_dict[len_s] = [(symbol, minima, name)]
    return s_dict


def compute_gs_int(t, x: np.ndarray, candidate_ss):
    for candidate_s in candidate_ss:
        m_s = candidate_s[1]
        candidate_coordinates = compute_coordinates(candidate_s[0])
        delta_x = x - candidate_coordinates
        h_x_ = h_x(x,candidate_coordinates,tau=get_tau(t))


def compute_sign(x: np.ndarray, candidate_coordinates: np.ndarray) -> np.ndarray:
    assert (
        x.shape == candidate_coordinates
    ), "Solution dimension and candidates dimension not match"
    differential = x - candidate_coordinates
    return differential / np.absolute(differential)


def h_x(
    x: np.ndarray,
    candidate_coordinates: np.ndarray,
    tau: int,
) -> np.ndarray:
    signs = compute_sign(
        x=x,
        candidate_coordinates=candidate_coordinates,
    )
    return signs / (4**tau)


def compute_coordinates(symbol_sequence: list, dim_space: int = 2) -> np.ndarray:
    coordinates = np.array([0 for _ in range(dim_space)])
    for index, symbol in enumerate(symbol_sequence):
        if abs(symbol) + 1 > dim_space:
            raise ValueError(
                f"Dimension cannot be greater than axis. Got dimension: {dim_space}, axis: {symbol}"
            )
        if symbol != 0:
            movement_length = symbol / abs(symbol) / (4 ** (index + 1))
            coordinates[abs(symbol) - 1] += movement_length
    return coordinates


def compute_f_t_x_int(x: np.ndarray, processed_sequence: dict):
    f_t_x = {}
    for t in range(max(processed_sequence.keys()) + 1):
        if t == 0:
            f_t_x[(t, x)] = 0
        else:
            tau = get_tau(t=t)
            candidate_f = f_t_x[(t, x)]
            candidate_ss = processed_sequence[tau]
            candidate_gxs = None
            # TODO: add gx computation here


if __name__ == "__main__":
    solution_variables = (1, 2, 3.9)
    sequence_info = [
        {"minima": 0.0, "attrs": {"symbol": [], "id": 0, "minima": 0.0}, "name": 0},
        {
            "minima": -1,
            "attrs": {"group": 0, "symbol": [1], "id": 1, "minima": -1},
            "name": 1,
        },
        {
            "minima": -20.78,
            "attrs": {"group": 0, "symbol": [1, -2, -1], "id": 2, "minima": -20.78},
            "name": 2,
        },
        {
            "minima": 33.75,
            "attrs": {"group": 0, "symbol": [1, -2, 1], "id": 3, "minima": 33.75},
            "name": 3,
        },
        {
            "minima": 31.75,
            "attrs": {"group": 0, "symbol": [1, -2], "id": 4, "minima": 31.75},
            "name": 4,
        },
    ]

    print(process_sequence(sequence=sequence_info))

    evaluate(
        solution_variables=solution_variables,
        sequence_info=sequence_info,
    )
