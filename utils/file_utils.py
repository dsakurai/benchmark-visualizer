import json


def read_json_tree(file_path: str):
    with open(file_path, "r") as json_file:
        tree_info = json.load(json_file)
    return tree_info


def tree_to_json(file_path: str, tree_info: dict):
    with open(file_path, "w") as json_file:
        json.dump(tree_info, json_file)
