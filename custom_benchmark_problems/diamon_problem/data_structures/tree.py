from pathlib import Path

import igraph
import json

from custom_benchmark_problems.diamon_problem.data_structures.link import Link
from custom_benchmark_problems.diamon_problem.data_structures.node import Node
from utils import file_utils


class Tree:
    def __init__(self, dim_space: int, **kwargs):
        kwargs["dim_space"] = dim_space
        # Create a directed graph with 0 vertex
        # https://igraph.org/python/api/latest/igraph.Graph.html#__init__
        self._tree = igraph.Graph(n=0, directed=True, graph_attrs=kwargs)
        self.counter = 0

    # Define how to print out this data structure
    def __str__(self):
        vertices = []
        for vertex in self._tree.vs:
            vertices.append(vertex.attributes())
        return json.dumps(({"vertices": vertices, "edges": self._tree.get_edgelist()}))

    def from_json(self, data_path: str):
        tree_data = file_utils.read_json_tree(data_path)
        nodes = tree_data["nodes"]
        edges = tree_data["links"]
        for node in nodes:
            self._tree.add_vertex(name=node.pop("id", None), minima=node.pop("minima", None), attrs=node)
        for edge in edges:
            self._tree.add_edge(source=edge.pop("source", None), target=edge.pop("target", None), attrs=edge)

    def to_json(self, file_path: str = None):
        nodes = []
        links = []
        for node in self._tree.vs:
            node["attrs"]["id"] = node["name"]
            node["attrs"]["minima"] = node["minima"]
            nodes.append(node["attrs"])
        for link in self._tree.es:
            link["attrs"]["source"] = link.source
            link["attrs"]["target"] = link.target
            links.append(link["attrs"])
        tree_info = {"nodes": nodes, "links": links}
        if file_path:
            file_utils.tree_to_json(file_path, tree_info)
        return tree_info

    # TODO: Tree to image, skipped function @ 20220830
    def to_image(self, file_name: str):
        pass

    # Interpret node to iGraph vertex, with attributes and edges appended
    def add_node(self, minima: float, link: Link = None, parent: Node = None, **kwargs) -> int:
        if self._tree.vcount() == 0:
            self._tree.add_vertex(name=self.root_id, minima=0, link=None)
        node_id = self._tree.add_vertex(name=None, minima=minima)
        return node_id

    def add_edge(self) -> int:
        pass

    def structure(self) -> dict:
        pass

    def evaluate(self):
        t = self.counter
        if t == 0:
            return 0
        else:
            pass
        self.counter += 1

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
    tree.to_json()


