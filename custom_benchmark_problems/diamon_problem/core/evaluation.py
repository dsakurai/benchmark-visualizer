import numpy as np


def __tau(t: float) -> int:
    return int(t - 1) if int(t) == t else int(t)


def __delta_t(t: float, tau: int) -> float:
    return min(t - tau, 1)


def __check_s(sequence: tuple, tau: int) -> bool:
    return True if len(sequence) == tau else False


def evaluate(
    solution_variables: tuple, sequence_info: tuple, candidate_coordinates: list
) -> np.ndarray:
    t = solution_variables[-1]
    tau = __tau(t)
    while __check_s(sequence=sequence_info, tau=tau):
        pass

    return np.array([])


if __name__ == "__main__":
    evaluate((1, 2, 9.9), (1, -2, 1), [1, 2])
