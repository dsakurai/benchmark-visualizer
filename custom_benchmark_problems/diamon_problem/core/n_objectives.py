import numpy as np

from custom_benchmark_problems.diamon_problem.core.evaluation import BMP, EvaluationResult


class NBMP:
    def __init__(self, sequence_info: list[dict], dim_space: int,n_objectives:int, rotate: bool = True, degrees: int = 45, clockwise: bool = True):
        self.bmp = BMP(sequence_info=sequence_info, dim_space=dim_space, rotate=False)
        self.n_objectives = n_objectives
        self.rotate = rotate
        # Define rotate matrix information here
        theta = np.radians(degrees)
        self.c, self.s = np.cos(theta), np.sin(theta)


    def evaluate(self, solution_variables: np.ndarray) -> EvaluationResult:
        np.linalg.multi_dot()
        pass

    def generate_rotation_matrix(self, dimension_index:int):
        if dimension_index <= 1:
            raise ValueError(f"Dimension {dimension_index} is not acceptable")
        base_matrix = np.identity(self.n_objectives)
        print(base_matrix)
        print(base_matrix[])

    def parse_variables(self, solution_variables: np.ndarray,dimension: int) -> np.ndarray:
        pass

if __name__ == "__main__":
    n_bmp = NBMP(sequence_info=[],dim_space=1, n_objectives=3,)
    n_bmp.generate_rotation_matrix(2)