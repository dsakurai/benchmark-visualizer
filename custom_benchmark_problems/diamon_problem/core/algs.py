from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree
from pathlib import Path

def compute_path(tree_data: dict):
    for node in tree_data["nodes"]:
        print(node)
    pass


def compute_node_tree():
    pass


if __name__ == "__main__":
    tree = Tree(dim_space=2)
    base_path = Path(__file__).parent.absolute().parents[2]
    data_path = base_path / "sample.json"
    print(data_path)
    tree.from_json(data_path)
    print(tree)
    tree.to_json()
    sequence = tree.read_path(7)
    tree.evaluate(sequence,[1.0,2.0])
