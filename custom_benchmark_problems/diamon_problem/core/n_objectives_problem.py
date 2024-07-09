from collections import namedtuple

import numpy as np

from custom_benchmark_problems.diamon_problem.core.evaluation import (
    BMP,
    EvaluationResult,
)

NEvaluationResult = namedtuple(
    "NEvaluationResult",
    ["objective_values", "node_id", "diagonal_length", "unrotated_value"],
)


class NBMP(BMP):
    def __init__(
        self,
        sequence_info: list[dict],
        dim_space: int,
        n_objectives: int,
        rotate: bool = False,
        domain_rotation: bool = False,
        degrees: int = -45,
        clockwise: bool = True,
    ):
        super().__init__(
            sequence_info=sequence_info, dim_space=dim_space, rotate=rotate
        )
        # self.bmp = BMP(sequence_info=sequence_info, dim_space=dim_space, rotate=False)
        self.n_objectives = n_objectives
        # self.rotate = rotate
        # # Define rotate matrix information here
        # theta = np.radians(degrees)
        # self.c, self.s = np.cos(theta), np.sin(theta)

    def n_evaluate(self, solution_variables: np.ndarray) -> NEvaluationResult:
        bmp_solution_variables, t_s = self.parse_variables(
            solution_variables=solution_variables
        )
        bmp_eval_res = self.evaluate(solution_variables=bmp_solution_variables)
        f_hat = bmp_eval_res.t
        f_1 = f_hat + self.l1_dist(reg_variables=t_s[1:])
        objective_values = np.concatenate(([f_1], t_s))
        return NEvaluationResult(
            objective_values=objective_values,
            node_id=bmp_eval_res.node_id,
            diagonal_length=bmp_eval_res.diagonal_length,
            unrotated_value=bmp_eval_res.unrotated_value,
        )

    # def generate_rotation_matrix(self, dimension_index: int):
    #     if dimension_index <= 1:
    #         raise ValueError(f"Dimension {dimension_index} is not acceptable")
    #     base_matrix = np.identity(self.n_objectives)
    #     print(base_matrix)
    #     base_matrix[0, 0] = self.c
    #     base_matrix[dimension_index - 1, 0] = self.s
    #     base_matrix[0, dimension_index - 1] = self.s
    #     base_matrix[dimension_index - 1, dimension_index - 1] = self.c
    #     print(base_matrix)

    @staticmethod
    def l1_dist(reg_variables: np.ndarray) -> float:
        return np.sum(np.abs(reg_variables))

    def parse_variables(
        self, solution_variables: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        # Variable format: [t_1, t_2, ... t_(n-1), x_1, x_2, ..., x_n]
        # Takes t_1 and all Xs for original BMP evaluation
        bmp_variables = np.concatenate(
            (solution_variables[:1], solution_variables[self.n_objectives - 1 :])
        )
        # Takes t_2 to t_(n-1) for the remaining computation
        t_s = solution_variables[: (self.n_objectives - 1)]
        return bmp_variables, t_s


if __name__ == "__main__":
    n_bmp = NBMP(
        sequence_info=[],
        dim_space=1,
        n_objectives=3,
    )
    n_bmp.generate_rotation_matrix(2)
