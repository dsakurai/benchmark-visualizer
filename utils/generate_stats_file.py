import sys

sys.path.append("../")

import os
from utils.file_utils import parse_meta
from tqdm import tqdm
import pandas as pd
import multiprocessing
from multiprocessing import Pool

search_dir = "../data"
exp_dir_pattern = "N-obj"

subdirs = [
    os.path.join(search_dir, d)
    for d in os.listdir(search_dir)
    if os.path.isdir(os.path.join(search_dir, d)) and d.startswith(exp_dir_pattern)
]

subdirs = []
for root, sub_dirs, files in os.walk("../data"):
    for sub_dir in sub_dirs:
        cwd = os.path.join(root, sub_dir)
        if sub_dir.startswith(exp_dir_pattern):
            subdirs.append(cwd)
        else:
            for sub_root, sub_sub_dirs, sub_files in os.walk(cwd):
                for sub_sub_dir in sub_sub_dirs:
                    if sub_sub_dir.startswith(exp_dir_pattern):
                        subdirs.append(os.path.join(cwd, sub_sub_dir))

meta_list = []
for subdir in subdirs:
    meta_list += parse_meta(exp_dir=subdir)

exp_df = pd.DataFrame(meta_list)


def parse_result_file(exp_file_path: str):
    result_df = pd.read_csv(exp_file_path)
    return result_df


dimensions = [2, 3, 4, 5]
n_objectives_list = [2, 3, 4, 5]
trees = ["breadth.json", "depth.json"]
solvers = ["MOEAD", "NSGAII", "GDE3", "OMOPSO", "IBEA"]
total_tasks = len(dimensions) * len(n_objectives_list) * len(trees)


def run_data(dimension, n_objectives, tree):
    print(f"Processing dimension {dimension}, n_objectives {n_objectives}")
    naming_prefix = f"dim{dimension}_objs{n_objectives}_tree_{tree.split('.')[0]}"
    stat_res = []
    for solver in solvers:
        filtered_df = exp_df[
            (exp_df["dimension"] == dimension)
            & (exp_df["n_objectives"] == n_objectives)
            & (exp_df["solver"] == solver)
            & (exp_df["tree"] == tree)
        ]
        for i, row in filtered_df.iterrows():
            eval_info = parse_result_file(row["exp_result_file"])
            try:
                vc = eval_info["eval_node_id"][99900:].value_counts()
                stat_res.append(
                    {
                        "solver": solver,
                        "exp_index": i,
                        "root": vc.get(0, 0),
                        "node_1": vc.get(1, 0),
                        "node_2": vc.get(2, 0),
                        "node_3": vc.get(3, 0),
                        "node_4": vc.get(4, 0),
                    }
                )
            except Exception as e:
                continue
    stat_res = pd.DataFrame(stat_res)
    stat_res.to_csv(naming_prefix + ".csv")


cpus = multiprocessing.cpu_count()
pool = Pool(processes=cpus)
pbar = tqdm(total=total_tasks)
pbar.set_description("Parsing Progress")


def pbar_update(*args):
    print(*args)
    pbar.update()


def print_err(value):
    print(f"ERR! {value}")
    pbar.update()


for dimension in dimensions:
    for n_objectives in n_objectives_list:
        for tree in trees:
            pool.apply_async(
                run_data,
                args=(
                    dimension,
                    n_objectives,
                    tree,
                ),
                error_callback=print_err,
                callback=pbar_update,
            )
pool.close()
pool.join()
pbar.close()
# run_data(dimension=dimension,n_objectives=n_objectives,tree=tree)
# print(f"Processing dimension {dimension}, n_objectives {n_objectives}")
# naming_prefix = (
#     f"dim{dimension}_objs{n_objectives}_tree_{tree.split('.')[0]}"
# )
# stat_res = []
# for solver in solvers:
#     filtered_df = exp_df[
#         (exp_df["dimension"] == dimension)
#         & (exp_df["n_objectives"] == n_objectives)
#         & (exp_df["solver"] == solver)
#         & (exp_df["tree"] == tree)
#     ]
#     for i, row in filtered_df.iterrows():
#         eval_info = parse_result_file(row["exp_result_file"])
#         try:
#             vc = eval_info["eval_node_id"][99900:].value_counts()
#             stat_res.append(
#                 {
#                     "solver": solver,
#                     "exp_index": i,
#                     "root": vc.get(0, 0),
#                     "node_1": vc.get(1, 0),
#                     "node_2": vc.get(2, 0),
#                     "node_3": vc.get(3, 0),
#                     "node_4": vc.get(4, 0),
#                     "node_5": vc.get(5, 0),
#                 }
#             )
#         except Exception as e:
#             continue
#     pbar.update(1)
# stat_res = pd.DataFrame(stat_res)
# stat_res.to_csv(naming_prefix + ".csv")
