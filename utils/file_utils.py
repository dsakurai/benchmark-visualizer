import json

import pandas as pd


def read_json_tree(file_path: str):
    with open(file_path, "r") as json_file:
        tree_info = json.load(json_file)
    return tree_info


def tree_to_json(file_path: str, tree_info: dict):
    with open(file_path, "w") as json_file:
        json.dump(tree_info, json_file)


def load_evaluation_log(file_path: str) -> list:
    eval_log = pd.read_csv(file_path, index_col=0)
    eval_log[["eval_node_id", "step"]] = eval_log[["eval_node_id", "step"]].astype(int)
    return eval_log.to_dict(orient="records")


if __name__ == "__main__":
    print(load_evaluation_log("../test_runx_2023-01-16T10-30-27.298413.csv"))
