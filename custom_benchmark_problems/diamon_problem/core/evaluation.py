import numpy as np

class BMP:
    def __init__(self, sequence_info: list, dim_space: int =2):
        self.sequence_info = sequence_info
        self.s_lengths = self.s_lengths(sequence_info)
        self.dim_space = dim_space
        self.f_t_x_ = {}

    def evaluate(self,solution_variables:np.ndarray):
        x = solution_variables[:-1]
        t = solution_variables[-1]
        return self.f_t_x(t=t,x=x,processed_sequence=self.process_sequence(sequence_info=self.sequence_info))

    @staticmethod
    def get_tau(t: float) -> int:
        """ Returns the corresponding tau for given t (tau<t<=tau+1, tau is int)

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

    def f_t_x(self,t, x: np.ndarray, processed_sequence: dict):
        if t == 0:
            return 0
        else:
            tau = self.get_tau(t)
            if (tau, tuple(x.tolist())) in self.f_t_x_.keys():
                return self.f_t_x_[(tau, tuple(x.tolist()))]
            while tau >= 0:
                if tau == 0:
                    delta_x = x
                    h_x_ = h_x(
                        x=x, candidate_coordinates=compute_coordinates([], 2), tau=tau
                    )
                    nabla_g = np.dot(
                        (-processed_sequence[tau][0][1] / h_x_), delta_x.T
                    ).item()
                    f_t_x_[(tau, tuple(x.tolist()))] = min(0, nabla_g)
                    return min(0, nabla_g)
                if tau not in processed_sequence.keys():
                    tau -= 1
                else:
                    f_tau_x = f_t_x(t=tau, x=x, processed_sequence=processed_sequence)
                    candidate_ss = processed_sequence[tau]
                    candidates = [f_tau_x]
                    for candidate_s in candidate_ss:
                        m_s = candidate_s[1]
                        delta_t = t - tau
                        # TODO: Change dim_space to dim space variable
                        candidate_coordinates = compute_coordinates(
                            symbol_sequence=candidate_s[0], dim_space=2
                        )
                        M_s = (1 - delta_t) * f_t_x(
                            tau, candidate_coordinates, processed_sequence
                        ) + delta_t * m_s
                        delta_x = x - candidate_coordinates
                        h_x_ = h_x(
                            x=x, candidate_coordinates=candidate_coordinates, tau=tau
                        )
                        nabla_g = (
                                          f_t_x(tau, candidate_coordinates + h_x_, processed_sequence)
                                          - m_s
                                  ) / h_x_
                        candidates.append(M_s + np.dot(nabla_g, delta_x.T))
                    f_t_x_[(t, tuple(x.tolist()))] = min(candidates)
                    return min(candidates)
    @staticmethod
    def process_sequence(sequence_info: list):
        """

        Parameters
        ----------
        sequence_info : list
            Extract sequence from a standard JSON format

        Returns
        -------

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
        """ Get the available symbol length of the entire sequence tree

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
        """ Get all symbol sequence at given length

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

    def __compute_f_taus(self) -> dict:
        """Compute all available f(tau,x) in advance

        Returns
        -------
        dict
            A dictionary with tau as key and values as list {tau:[{f(tau,x)}]}
        """
        f_taus = {}
        for s_length in self.s_lengths:
            f_taus[s_length] = self.__f_tau_x(
                s_length,self. get_s_at_length(self.sequence_info, s_length)
            )
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
    def __compute_sign(
        solution_variables: np.ndarray, candidate_coordinates: np.ndarray
    ) -> np.ndarray:
        assert (
            solution_variables.shape == candidate_coordinates
        ), "Solution dimension and candidates dimension not match"
        differential = solution_variables - candidate_coordinates
        return differential / np.absolute(differential)

    def __h_x(
        self,
        solution_variables: np.ndarray,
        candidate_coordinates: np.ndarray,
        tau: int,
    ) -> np.ndarray:
        signs = self.__compute_sign(
            solution_variables=solution_variables,
            candidate_coordinates=candidate_coordinates,
        )
        return signs / (4**tau)

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
        h_x = self.__h_x(
            solution_variables=x, candidate_coordinates=xs_coordinates, tau=tau
        )
        return (self.f_tau_x(tau, xs_coordinates + h_x) - m_s) / h_x

    @property
    def max_s_length(self) -> int:
        return max(self.s_lengths)

    def f_tau_x(self, tau: int, x: np.ndarray) -> np.ndarray:
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
                return self.f_tau_x(tau - 1, x)



if __name__ == "__main__":
    bmp = BMP(        sequence_info=[
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
        ],)
    bmp.f_t_x(
        solution_variables=(1, 2, 3.9),

        candidate_coordinates=[1, 2],
    )
