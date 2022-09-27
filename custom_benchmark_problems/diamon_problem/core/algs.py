from pathlib import Path

from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


def compute_links(tree_data: dict):
    links_info = []
    sorted_tree = sorted(tree_data["nodes"], key=lambda x: x['symbol'])
    sorted_tree.reverse()
    for index, node in enumerate(sorted_tree):
        if node["id"] == 0:
            continue
        previous_node = find_previous_node(node, index, sorted_tree)
        if previous_node:
            links_info.append({"source": previous_node["id"], "target": node["id"]})
        else:
            links_info.append({"source": 0, "target": node["id"]})
    return links_info


def find_previous_node(current_node, index, sorted_tree):
    for i in range(index, len(sorted_tree) - 1):
        if check_sublist(sorted_tree[i + 1]["symbol"], current_node["symbol"]):
            return sorted_tree[i + 1]


def check_sublist(new_list, org_list):
    # TODO: Naive implementation, may need to change
    iter_length = len(new_list) if len(new_list) < len(org_list) else len(org_list)
    for i in range(iter_length):
        if new_list[i] != org_list[i]:
            return False
    return True


if __name__ == "__main__":
    tree = Tree(dim_space=2)
    base_path = Path(__file__).parent.absolute().parents[2]
    data_path = base_path / "sample.json"
    tree.from_json(str(data_path))
    tree.load_edge(compute_links(tree.to_json()))
    print(tree)
    # sequence = tree.read_path(2)
    # tree.evaluate(sequence, [1.0, 2.0])
