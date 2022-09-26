from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree
from pathlib import Path


def compute_path(tree_data: dict):
    info_list = []
    for node in tree_data["nodes"]:
        print(node)
        print(node["symbol"][-1])
        info_list.append(node["symbol"])
        print("**")
    info_list = sorted(info_list)
    max_len = len(info_list[-1])
    links = []
    for sym in info_list:
        sym.insert(0, 0)
        if sym not in links:
            links.append(sym)
    print(links)
    max_len -= 1


def compare_sequence(links, symbol):
    pass


if __name__ == "__main__":
    tree = Tree(dim_space=2)
    base_path = Path(__file__).parent.absolute().parents[2]
    data_path = base_path / "sample.json"
    tree.from_json(data_path)
    print(tree)
    compute_path(tree.to_json())
    sequence = tree.read_path(2)
    tree.evaluate(sequence, [1.0, 2.0])
