import os
import time
from argparse import ArgumentParser

from tqdm import tqdm


def main(opts):
    # Number of experiments
    n_exps = 5
    exp_base_name = "multi_exps"
    for index in range(n_exps):
        exp_name = f"{exp_base_name}_{index}"
        contents[
            -1
        ] = f"python lmm-qsar.py --ito --num_iters {args.num_iters} --starting_point {start} --fragment_size {args.fragment_size} --input_file {opts.exp_file_path}"
        job_file_name = f"ito_exp_qsar_batch_{start}-{start + args.fragment_size}.sh"
        batch_jobs.append(job_file_name)
        with open(job_file_name, "w") as file:
            file.writelines(contents)
    base_file.close()

    for index, job_name in tqdm(
        enumerate(batch_jobs), total=len(batch_jobs), desc="Batch progress"
    ):
        os.system(f"pjsub {job_name}")
        time.sleep(60)
        # if (index + 1) % 16 == 0:
        #     time.sleep(10 * 3600)
        # else:
        #     time.sleep(30)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("exp_file_path", type=str)
    parser.add_argument("--n_nodes", type=int, default=16)
    parser.add_argument("--fragment_size", type=int, default=100)
    parser.add_argument("--num_iters", type=int, default=50000)
    args = parser.parse_args()
    main(args)
