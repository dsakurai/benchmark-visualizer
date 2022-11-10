import numpy as np

from algs import *


class BMP:
    def __init__(self, sequence_info: list):
        self.sequence_info = sequence_info
        self.s_lengths = s_lengths(sequence_info)
        self.f_taus = self.__compute_f_taus()

    @staticmethod
    def __tau(t: float) -> int:
        return int(t - 1) if int(t) == t else int(t)

    def __compute_f_taus(self) -> dict:
        """ Compute all available f(tau,x) in advance

        Returns
        -------
        dict
            A dictionary with tau as key and values as list {tau:[{f(tau,x)}]}
        """
        f_taus = {}
        for s_length in self.s_lengths:
            f_taus[s_length] = self.__f_tau_x(s_length, get_s_at_length(self.sequence_info, s_length))
        return f_taus

    @staticmethod
    def __f_tau_x(tau: int, s_at_taus: list) -> list:
        """Compute f(tau,x) with a guarantee of |s|=tau exists

        Parameters
        ----------
        tau : int
            tau value
        s_at_taus : list
            List of sequence information @ |s|=tau
        Returns
        -------
        list
            List of values @ f(tau,x)
        """
        ms_ts = []
        # f(t,x)=0 for t=0
        if tau == 0:
            return [0]
        for s_at_tau in s_at_taus:
            ms_t = s_at_tau["minima"]
            ms_ts.append(ms_t)
        return ms_ts

    @staticmethod
    def __compute_sign(solution_variables: np.ndarray, candidate_coordinates: np.ndarray) -> np.ndarray:
        assert (
                solution_variables.shape == candidate_coordinates
        ), "Solution dimension and candidates dimension not match"
        differential = solution_variables - candidate_coordinates
        return differential / np.absolute(differential)

    def __h_x(self, solution_variables: np.ndarray, candidate_coordinates: np.ndarray, tau: int) -> np.ndarray:
        signs = self.__compute_sign(
            solution_variables=solution_variables,
            candidate_coordinates=candidate_coordinates,
        )
        return signs / (4 ** tau)

    @staticmethod
    def __compute_coordinates(symbol_sequence: list, dim_space: int) -> np.ndarray:
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

    @staticmethod
    def __delta_t(t: float, tau: int) -> float:
        return min(t - tau, 1)

    def __nabla_g(self, x: np.ndarray, xs_coordinates: np.ndarray, tau: int, s: dict):
        m_s = s["minima"]
        h_x = self.__h_x(solution_variables=x, candidate_coordinates=xs_coordinates, tau=tau)
        return (self.f_tau_x(tau, xs_coordinates+h_x) - m_s) / h_x

    @property
    def max_s_length(self) -> int:
        return max(self.s_lengths)

    def f_tau_x(self, tau: int, x: np.ndarray):
        """Recursively compute tau until condition is hit

        Parameters
        ----------
        tau : int
            tau value
        x : np.ndarray
            Variables other than t

        Returns
        -------
        list
            List of values @ f(tau,x)
        """
        if tau == 0:
            return np.array([0])
        else:
            if tau in self.s_lengths:
                return self.f_taus[tau]
            else:
                return self.f_tau_x(tau - 1,x)


def evaluate(
        solution_variables: tuple, sequence_info: list, candidate_coordinates: list
) -> np.ndarray:
    t = solution_variables[-1]
    x = solution_variables[:-1]
    problem = BMP(sequence_info=sequence_info)

    if t > problem.max_s_length + 1:
        tau = problem.max_s_length
        # TODO: compute f(tau,x)
    else:
        # TODO: compute f(t,x)
        pass
    return np.array([])


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
