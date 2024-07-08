import json
import math, os
from pathlib import Path

import pandas as pd
from utils.log import Logger


def read_json_tree(file_path: str) -> dict:
    with open(file_path, "r") as json_file:
        tree_info = json.load(json_file)
    return tree_info


def tree_to_json(file_path: str, tree_info: dict) -> None:
    with open(file_path, "w") as json_file:
        json.dump(tree_info, json_file)


def load_evaluation_log(file_path: str) -> list:
    Logger().debug.info(f"Loading data from disk, file size {get_file_size(file_path)}")
    eval_log = pd.read_csv(file_path, index_col=0)
    eval_log[["eval_node_id", "step"]] = eval_log[["eval_node_id", "step"]].astype(int)
    Logger().debug.info("Load complete, processing ...... ")
    return eval_log[
        ["t", "y1", "y2", "eval_node_id", "diagonal_length", "step", "t_org", "y_org"]
    ].to_dict(orient="records")


def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
        return file_size
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"


def convert_size(size_bytes):
    if size_bytes == "File not found" or isinstance(size_bytes, str):
        return size_bytes
    elif size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def parse_exp_dir_with_meta(
    data_path, file_name_pattern: str
) -> tuple[Path, Path, Path] | None:
    entries = os.listdir(data_path)
    subdirectories = [
        entry for entry in entries if os.path.isdir(os.path.join(data_path, entry))
    ]
    for sub_dir in subdirectories:
        if sub_dir.startswith(file_name_pattern):
            exp_file_path = Path(sub_dir) / (sub_dir + ".csv")
            exp_tree = Path(sub_dir) / "meta" / "experiment_tree.json"
            meta_data = Path(sub_dir) / "meta" / "meta.json"
            return exp_file_path, exp_tree, meta_data

    Logger().debug.error(
        f"File or directory {data_path} for pattern {file_name_pattern} not found."
    )
    return None


if __name__ == "__main__":
    print(parse_exp_dir_with_meta("../data/test_exp_v8", "NSGAII"))
    # print(load_evaluation_log("../test_runx_2023-01-16T10-30-27.298413.csv"))
