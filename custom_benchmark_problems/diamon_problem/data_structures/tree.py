import json
import math
from pathlib import Path
from typing import NamedTuple, List

import igraph

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
        for node in nodes:
            self._tree.add_vertex(name=node.pop("id", None), minima=node.pop("minima", None), attrs=node)
        if "links" in tree_data:
            edges = tree_data["links"]
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

    def read_path(self, node_id: int):
        class SequenceInfo(NamedTuple):
            node_id: int
            minima: float
            axis: int
            direction: int

        path_sequence = []

        def get_parent(current_id: int):
            current_vertex = self._tree.vs[current_id]
            edge_info = current_vertex.in_edges()[0]
            up_link = Link(edge_info)
            path_sequence.append(SequenceInfo(current_id, Node(current_vertex).minima, up_link.axis, up_link.direction
                                              ))
            return edge_info.source

        current_node = self._tree.vs[node_id]
        if current_node.out_edges():
            # TODO: Change this to warning
            print("Not terminal node")

        while node_id != 0:
            source_node = get_parent(node_id)
            node_id = source_node

        path_sequence.append(SequenceInfo(self.root_node.node_id, self.root_node.minima, 0, 0))
        return path_sequence

    def evaluate(self, path_sequence: list, xs: List[float]):
        print(path_sequence)
        s_length = len(path_sequence) - 1
        ms = path_sequence[0][1]
        t = self.counter
        if t == 0:
            return 0
        else:
            pass
        self.counter += 1
        for i, x in enumerate(xs):
            h_i_tau = math.copysign(1 / 4 ** s_length, x)

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
    sequence = tree.read_path(7)
    tree.evaluate(sequence, [1.0, 2.0])
