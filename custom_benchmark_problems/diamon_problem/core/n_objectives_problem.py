import numpy as np

from custom_benchmark_problems.diamon_problem.core.evaluation import (
    BMP,
    EvaluationResult,
)


class NBMP(BMP):
    def __init__(
        self,
        sequence_info: list[dict],
        dim_space: int,
        n_objectives: int,
        rotate: bool = False,
        degrees: int = -45,
        clockwise: bool = True,
    ):
        super().__init__(sequence_info=sequence_info, dim_space=dim_space,rotate=rotate)
        # self.bmp = BMP(sequence_info=sequence_info, dim_space=dim_space, rotate=False)
        self.n_objectives = n_objectives
        # self.rotate = rotate
        # # Define rotate matrix information here
        # theta = np.radians(degrees)
        # self.c, self.s = np.cos(theta), np.sin(theta)

    def n_evaluate(self, solution_variables: np.ndarray) -> EvaluationResult:
        t_s, x_s = self.parse_variables(solution_variables=solution_variables)
        bmp_solution_variables =
        bmp_eval_res = self.evaluate()

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

    def parse_variables(
        self, solution_variables: np.ndarray
    ) -> tuple[np.ndarray,np.ndarray]:
        #  Variable format: [t_1, t_2, ... t_(n-1), x_1, x_2, ..., x_n]
        t_s = solution_variables[:(self.n_objectives - 1)]
        x_s = solution_variables[self.n_objectives - 1:]
        return t_s, x_s


if __name__ == "__main__":
    n_bmp = NBMP(sequence_info=[],dim_space=1, n_objectives=3,)
    n_bmp.generate_rotation_matrix(2)
