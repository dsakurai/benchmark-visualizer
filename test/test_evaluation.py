import unittest

import numpy as np
from numpy.testing import assert_almost_equal

from custom_benchmark_problems.diamon_problem.core import evaluation


class TestEvaluation(unittest.TestCase):
    def test_evaluate(self):
        bmp = evaluation.BMP(
            sequence_info=[
                {
                    "minima": -0.5,
                    "attrs": {"symbol": [], "id": 0, "minima": -0.5},
                    "name": 0,
                },
                {
                    "minima": -0.4,
                    "attrs": {"symbol": [1], "id": 0, "minima": -0.4},
                    "name": 0,
                },
            ],
            dim_space=1,
        )
        x_ts = [
            [0, 0],
            [0, 0.5],
            [0, 1],
            [0.5, 0],
            [0.5, 1],
            [0.5, 1.5],
            [0.5, 2],
            [0.25, 0],
            [0.25, 0.5],
            [0.25, 1],
            [0.25, 1.5],
            [0.75, 0],
            [0.75, 0.5],
            [0.75, 1],
            [0.75, 1.5],
        ]
        y_s = [
            (0.0, 0.0),
            (0.0, 0.0),
            (0.0, 0.0),
            (0.1767766952966369, -0.5303300858899107),
            (0.3535533905932738, -0.3535533905932738),
            (0.3535533905932738, -0.3535533905932738),
            (0.3535533905932738, -0.3535533905932738),
            (0.08838834764831845, -0.26516504294495535),
            (0.1767766952966369, -0.1767766952966369),
            (0.1767766952966369, -0.1767766952966369),
            (0.1767766952966369, -0.1767766952966369),
            (0.26516504294495535, -0.7954951288348661),
            (0.4419417382415923, -0.6187184335382292),
            (0.5303300858899107, -0.5303300858899107),
            (0.5303300858899107, -0.5303300858899107),
        ]
        for x_t, y in zip(x_ts, y_s):
            assert_almost_equal(
                y,
                bmp.evaluate(solution_variables=np.array(x_t, dtype="float64"))[:2],
                decimal=16,
            )
