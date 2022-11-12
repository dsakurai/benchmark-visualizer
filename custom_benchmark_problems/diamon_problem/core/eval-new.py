import numpy as np

from algs import *


class BMP:
    def __init__(self, sequence_info: list):
        self.sequence_info = sequence_info
        self.s_lengths = s_lengths(sequence_info)


def evaluate(
    solution_variables: tuple, sequence_info: list, candidate_coordinates: list
) -> np.ndarray:
    t = solution_variables[-1]
    x = solution_variables[:-1]
    tau = get_tau(t)
    problem = BMP(sequence_info=sequence_info)

    while True:
        if tau in problem.s_lengths:
            pass
        else:
            tau -= 1

if __name__ == "__main__":
    evaluate(
        solution_variables=(1, 2, 3.9),
        sequence_info=[
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
        ],
        candidate_coordinates=[1, 2],
    )
