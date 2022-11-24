import numpy as np
from algs import *


class Evaluate:
    def __init__(self, solution_variables: np.ndarray, sequence_info: list):
        self.x = solution_variables[:-1]
        self.t = solution_variables[-1]
        self.dim_space = solution_variables.shape[0] - 1
        self.processed_sequence = self.process_sequence(sequence=sequence_info)
        self.f_t_x_ = {}

    @staticmethod
    def compute_sign(x: np.ndarray, candidate_coordinates: np.ndarray) -> np.ndarray:
        # assert (
        #         x.shape == candidate_coordinates
        # ), "Solution dimension and candidates dimension not match"
        # TODO: Confirm if this is set to 1 if 0s were given
        differential = x - candidate_coordinates
        differential = np.where(differential != 0, differential, 1)
        return np.divide(differential, np.absolute(differential))

    @staticmethod
    def process_sequence(sequence: list):
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

    def h_x(
        self,
        x: np.ndarray,
        candidate_coordinates: np.ndarray,
        tau: int,
    ) -> np.ndarray:
        signs = self.compute_sign(
            x=x,
            candidate_coordinates=candidate_coordinates,
        )
        return signs / (4**tau)

    @staticmethod
    def compute_coordinates(symbol_sequence: list, dim_space: int = 2) -> np.ndarray:
        coordinates = np.array([0 for _ in range(dim_space)])
        for index, symbol in enumerate(symbol_sequence):
            print(symbol)
            if abs(symbol) > dim_space:
                raise ValueError(
                    f"Dimension cannot be greater than axis. Got dimension: {dim_space}, axis: {symbol}"
                )
            if symbol != 0:
                movement_length = symbol / abs(symbol) / (4 ** (index + 1))
                coordinates[abs(symbol) - 1] += movement_length
        return coordinates

    def f_t_x(self, t, x: np.ndarray, processed_sequence: dict, dim_space: int):
        if t == 0:
            return 0
        else:
            tau = get_tau(t)
            if (tau, tuple(x.tolist())) in self.f_t_x_.keys():
                return self.f_t_x_[(tau, tuple(x.tolist()))]
            while tau >= 0:
                if tau == 0:
                    delta_x = x
                    h_x_ = self.h_x(
                        x=x,
                        candidate_coordinates=self.compute_coordinates([], 2),
                        tau=tau,
                    )
                    nabla_g = np.dot(
                        (-processed_sequence[tau][0][1] / h_x_), delta_x.T
                    ).item()
                    self.f_t_x_[(tau, tuple(x.tolist()))] = min(0, nabla_g)
                    return min(0, nabla_g)
                if tau not in processed_sequence.keys():
                    tau -= 1
                else:
                    f_tau_x = self.f_t_x(
                        t=tau,
                        x=x,
                        processed_sequence=processed_sequence,
                        dim_space=dim_space,
                    )
                    candidate_ss = processed_sequence[tau]
                    candidates = [f_tau_x]
                    for candidate_s in candidate_ss:
                        m_s = candidate_s[1]
                        delta_t = t - tau
                        # TODO: Change dim_space to dim space variable
                        candidate_coordinates = self.compute_coordinates(
                            symbol_sequence=candidate_s[0], dim_space=dim_space
                        )
                        M_s = (1 - delta_t) * self.f_t_x(
                            tau,
                            candidate_coordinates,
                            processed_sequence,
                            dim_space=dim_space,
                        ) + delta_t * m_s
                        delta_x = x - candidate_coordinates
                        h_x_ = self.h_x(
                            x=x, candidate_coordinates=candidate_coordinates, tau=tau
                        )
                        nabla_g = (
                            self.f_t_x(
                                tau,
                                candidate_coordinates + h_x_,
                                processed_sequence,
                                dim_space=dim_space,
                            )
                            - m_s
                        ) / h_x_
                        candidates.append(M_s + np.dot(nabla_g, delta_x.T))
                    self.f_t_x_[(t, tuple(x.tolist()))] = min(candidates)
                    return min(candidates)
