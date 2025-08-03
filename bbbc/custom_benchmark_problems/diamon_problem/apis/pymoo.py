import numpy as np
from pymoo.core.problem import Problem


class MyProblem(Problem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, xl=-2.0, xu=2.0)

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = 100 * (x[:, 0] ** 2 + x[:, 1] ** 2)
        f2 = (x[:, 0] - 1) ** 2 + x[:, 1] ** 2
        out["F"] = np.column_stack([f1, f2])
