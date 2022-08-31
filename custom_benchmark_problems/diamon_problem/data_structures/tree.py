from pathlib import Path

import igraph
import json

from custom_benchmark_problems.diamon_problem.data_structures.movement import Movement
from custom_benchmark_problems.diamon_problem.data_structures.node import Node
from utils.file_utils import read_json_tree


class Tree:
    def __init__(self, dim_space: int, **kwargs):
        kwargs["dim_space"] = dim_space
        # Create a directed graph with 0 vertex
        # https://igraph.org/python/api/latest/igraph.Graph.html#__init__
        self._tree = igraph.Graph(n=0, directed=True, graph_attrs=kwargs)

    def __str__(self):
        vertices = []
        for vertex in self._tree.vs:
            vertices.append(vertex)
            print(vertex.attributes())
        return json.dumps(({"vertices":vertices, "edges":self._tree.get_edgelist()}))

    def from_json(self, data_path: str):
        tree_data = read_json_tree(data_path)
        print(tree_data)
        nodes = tree_data["nodes"]
        edges = tree_data["links"]
        node_ids = [node["id"] for node in nodes]
        node_minimas = [node["minima"] for node in nodes]
        for node in nodes:
            self._tree.add_vertex(name=node.pop("id", None), minima=node.pop("minima", None), attrs=node)
        for edge in edges:
            self._tree.add_edge(source=edge.pop("source", None), target=edge.pop("target", None), attrs=edge)

    def to_json(self):
        pass

    def to_image(self, file_name: str):
        pass

    def add_node(self, movement: Movement = None, parent: Node = None) -> int:
        pass

    def add_edge(self) -> int:
        pass

    def structure(self) -> dict:
        pass

    @property
    def dim_space(self) -> int:
        return self._tree["dim_space"]

    @property
    def root_id(self) -> int:
        return 0

    @property
    def root_node(self) -> Node:
        return Node(self._tree.vs[self.root_id])


if __name__ == "__main__":
    tree = Tree(dim_space=2)
    base_path = Path(__file__).parent.absolute().parents[2]
    data_path = base_path / "sample.json"
    tree.from_json(data_path)
    print(tree)
