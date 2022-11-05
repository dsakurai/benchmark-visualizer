import numpy as np


def __tau(t: float) -> int:
    return int(t - 1) if int(t) == t else int(t)


def __delta_t(t: float, tau: int) -> float:
    return min(t - tau, 1)


def __s_subset(sequence_info: tuple, t) -> tuple:
    assert t <= __max_s_length(sequence_info) + 1, "t has exceeded maxmium value"
    yield sequence_info


def __max_s_length(sequence_info: tuple) -> int:
    return len(sequence_info)


def evaluate(
    solution_variables: tuple, sequence_info: tuple, candidate_coordinates: list
) -> np.ndarray:
    t = solution_variables[-1]
    x = solution_variables[:-1]
    max_s_length = __max_s_length(sequence_info)
    if t > max_s_length + 1:
        tau = max_s_length
        # TODO: compute f(tau,x)
    else:
        # TODO: compute f(t,x)
        pass
    return np.array([])

    return np.array([])


if __name__ == "__main__":
    evaluate((1, 2, 9.9), (1, -2, 1), [1, 2])
