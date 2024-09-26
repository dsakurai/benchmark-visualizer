import sys

sys.path.append("../")

import os
import glob
from utils.reference_fronts import ReferenceFronts
from utils.file_utils import parse_exp_log_dir, load_n_evaluation_log, parse_meta
from utils.performance_evaluator import PerformanceEvaluator
from tqdm import tqdm
import pandas as pd

search_dir = "../data"
exp_dir_pattern = "N-obj"

subdirs = [
    os.path.join(search_dir, d)
    for d in os.listdir(search_dir)
    if os.path.isdir(os.path.join(search_dir, d)) and d.startswith(exp_dir_pattern)
]

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
total_tasks = len(dimensions) * len(n_objectives_list) * len(trees) * len(solvers)

with tqdm(total=total_tasks, desc="Total progress") as pbar:
    for dimension in dimensions:
        for n_objectives in n_objectives_list:
            for tree in trees:
                print(f"Processing dimension {dimension}, n_objectives {n_objectives}")
                naming_prefix = (
                    f"dim{dimension}_objs{n_objectives}_tree_{tree.split('.')[0]}"
                )
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
                                    "node_5": vc.get(5, 0),
                                }
                            )
                        except Exception as e:
                            continue
                    pbar.update(1)
                stat_res = pd.DataFrame(stat_res)
                stat_res.to_csv(naming_prefix + ".csv")
