import json


def read_json_tree(file_path: str):
    with open(file_path, "r") as json_file:
        tree_info = json.load(json_file)
    return tree_info
