import numpy as np


class BMP:
    def __init__(self, sequence_info: list, dim_space: int = 2):
        self.sequence_info = sequence_info
        self.s_lengths = self.s_lengths(sequence_info)
        self.dim_space = dim_space
        self.f_t_x_ = {}

    def evaluate(self, solution_variables: np.ndarray):
        x = solution_variables[:-1]
        t = solution_variables[-1]
        return self.f_t_x(
            t=t,
            x=x,
            processed_sequence=self.process_sequence(sequence_info=self.sequence_info),
        )

    def h_x(
            self,
            x: np.ndarray,
            candidate_coordinates: np.ndarray,
            tau: int,
    ) -> np.ndarray:
        """Compute h(x) with solution variables and candidate coordinates and tau

        Parameters
        ----------
        x : np.ndarray
            Solution variables without t
        candidate_coordinates: np.ndarray
            Coordinates of the local minima point
        tau : int
            tau value

        Returns
        -------
        np.ndarray
            A numpy array representing h(x) in each dimension
        """
        signs = self.compute_sign(
            x=x,
            candidate_coordinates=candidate_coordinates,
        )
        return signs / (4 ** tau)

    def compute_coordinates(self, symbol_sequence: list) -> np.ndarray:
        """Compute the coordinates for the given symbol sequence.

        Parameters
        ----------
        symbol_sequence: list
            List of ints representing the symbol sequence

        Returns
        -------
        np.ndarray
            The coordinates of the given symbol sequence, each element representing value in corresponding dimension
        """
        coordinates = np.array([0 for _ in range(self.dim_space)])
        for index, symbol in enumerate(symbol_sequence):
            if abs(symbol) > self.dim_space:
                raise ValueError(
                    f"Dimension cannot be greater than axis. Got dimension: {self.dim_space}, axis: {symbol}"
                )
            if symbol != 0:
                movement_length = symbol / abs(symbol) / (4 ** (index + 1))
                coordinates[abs(symbol) - 1] += movement_length
        return coordinates

    @staticmethod
    def compute_sign(x: np.ndarray, candidate_coordinates: np.ndarray) -> np.ndarray:
        """Compute the sign of x with regard to local minima point x_s, if x is the local minima point, then the sign
        will be set to positive (1 in practice)

        Parameters
        ----------
        x : np.ndarray
            Solution variables
        candidate_coordinates : np.ndarray
            The coordinates of the local minima point

        Returns
        -------
        np.ndarray
            The sign in each dimension
        """
        differential = x - candidate_coordinates
        differential = np.where(differential != 0, differential, 1)
        return np.divide(differential, np.absolute(differential))

    @staticmethod
    def get_tau(t: float) -> int:
        """Returns the corresponding tau for given t (tau<t<=tau+1, tau is int)

        Parameters
        ----------
        t : float
            t value

        Returns
        -------
        int
            tau value
        """
        return int(t - 1) if int(t) == t else int(t)

    @staticmethod
    def process_sequence(sequence_info: list):
        """Pre-process the sequence and group symbol sequence with the same size togather

        Parameters
        ----------
        sequence_info : list
            Extract sequence from a standard JSON format

        Returns
        -------
        dict
            Dictionary with length as key and list of tuple(symbol, minima, name) as value
        """
        # TODO: Change naming here, don't want to do this right now
        s_dict = {}
        for item in sequence_info:
            minima = item["minima"]
            symbol = item["attrs"]["symbol"]
            name = item["name"]
            len_s = len(symbol)
            if len_s in s_dict:
                s_dict[len_s].append((symbol, minima, name))
            else:
                s_dict[len_s] = [(symbol, minima, name)]
        return s_dict

    @staticmethod
    def s_lengths(sequence_info: list) -> list:
        """Get the available symbol length of the entire sequence tree

        Parameters
        ----------
        sequence_info : list
            List of dictionaries contains the tree information

        Returns
        -------
        list
            List of the available symbol lengths

        """
        # TODO: Naive implementation
        length_list = []
        for element in sequence_info:
            if len(element["attrs"]["symbol"]) not in length_list:
                length_list.append(len(element["attrs"]["symbol"]))
        return length_list

    @staticmethod
    def get_s_at_length(sequence_info: list, length: int) -> list:
        """Get all symbol sequence at given length

        Parameters
        ----------
        sequence_info : list
            List of dictionaries contains the tree information
        length : int
            The desired length

        Returns
        -------
        list
            List of sequence information at given length
        """
        s_list = []
        for element in sequence_info:
            if len(element["attrs"]["symbol"]) == length:
                s_list.append(element)
        return s_list

    def f_t_x(self, t: int, x: np.ndarray, processed_sequence: dict) -> float:
        if t == 0:
            return 0.0
        else:
            tau = self.get_tau(t)
            # if (tau, tuple(x.tolist())) in self.f_t_x_.keys():
            #     return self.f_t_x_[(tau, tuple(x.tolist()))]
            while tau >= 0:
                if tau not in processed_sequence.keys():
                    return self.f_t_x(t=tau, x=x, processed_sequence=processed_sequence)
                else:
                    f_tau_x = self.f_t_x(
                        t=tau, x=x, processed_sequence=processed_sequence
                    )
                    candidate_ss = processed_sequence[tau]
                    candidates = [f_tau_x]
                    for candidate_s in candidate_ss:
                        m_s = candidate_s[1]
                        delta_t = t - tau
                        candidate_coordinates = self.compute_coordinates(
                            symbol_sequence=candidate_s[0]
                        )
                        M_s = (1 - delta_t) * self.f_t_x(
                            tau, candidate_coordinates, processed_sequence
                        ) + delta_t * m_s
                        delta_x = x - candidate_coordinates
                        h_x_ = self.h_x(
                            x=x, candidate_coordinates=candidate_coordinates, tau=tau
                        )
                        nabla_g = (
                                          self.f_t_x(
                                              tau, candidate_coordinates + h_x_, processed_sequence
                                          )
                                          - m_s
                                  ) / h_x_
                        candidates.append(M_s + np.dot(nabla_g, delta_x.T))
                    # self.f_t_x_[(t, tuple(x.tolist()))] = min(candidates)
                    return min(candidates)


if __name__ == "__main__":
    bmp = BMP(
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
        dim_space=2,
    )
    print(
        bmp.evaluate(
            solution_variables=np.array([1, 2, 3.9]),
        )
    )
