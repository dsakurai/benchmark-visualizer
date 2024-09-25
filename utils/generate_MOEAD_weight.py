import argparse
import math

import numpy as np
from scipy.stats import qmc
from quasimc.sobol import Sobol


def generate(
    n_dims: int, n_rows: int, file_path: str, bits: int = None, method: str = "scipy"
):
    if method == "scipy":
        n_power = math.ceil(math.log2(100))
        sampler = qmc.Sobol(d=n_dims, scramble=True, bits=bits)
        generated_arr = sampler.random_base2(n_power)[
            : n_rows - n_dims,
        ]
    elif method == "quasimc":
        import time

        seed = int(time.time() * 10000000 % 10000)
        sobol = Sobol(dim=n_dims, seed=seed)
        generated_arr = sobol.generate(n_rows - n_dims).T
    else:
        raise NotImplementedError(f"Invalid method {method}")
    base_arr = np.eye(n_dims)
    generated_arr = np.vstack((base_arr, generated_arr))
    np.savetxt(file_path, generated_arr, fmt="%.16f", delimiter=" ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n_dims", type=int)
    parser.add_argument("n_rows", type=int)
    parser.add_argument("file_path", type=str)
    parser.add_argument("method", type=str)
    parser.add_argument("--bits", type=int, required=False, default=None)
    args = parser.parse_args()
    generate(
        n_rows=args.n_rows,
        file_path=args.file_path,
        n_dims=args.n_dims,
        method=args.method,
    )
