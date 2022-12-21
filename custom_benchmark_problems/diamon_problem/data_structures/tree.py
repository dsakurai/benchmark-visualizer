import json
from pathlib import Path
from typing import NamedTuple, Union

import igraph

from custom_benchmark_problems.diamon_problem.data_structures.link import Link
from custom_benchmark_problems.diamon_problem.data_structures.node import Node
from custom_benchmark_problems.diamon_problem.core.validators import (
    validate_tree_minima,
)
from utils import file_utils


class Tree:
    def __init__(self, dim_space: int, **kwargs):
        kwargs["dim_space"] = dim_space
        # Create a directed graph with 0 vertex
        # https://igraph.org/python/api/latest/igraph.Graph.html#__init__
        self._tree = igraph.Graph(n=0, directed=True, graph_attrs=kwargs)
        self._tree.add_vertex(
            name=self.root_id,
            minima=self.root_minima,
            attrs={"symbol": self.root_symbol},
        )
        self.counter = 0

    # Define how to print out this data structure
    def __str__(self):
        vertices = []
        for vertex in self._tree.vs:
            vertices.append(vertex.attributes())
        return json.dumps(({"vertices": vertices, "edges": self._tree.get_edgelist()}))

    def __validate(self):
        sequence_data = self.to_sequence()
        validate_tree_minima(sequence_data=sequence_data, dim_space=self.dim_space)

    def from_dict(self, tree_data: dict):
        nodes = tree_data["nodes"]
        for node in nodes:
            self._tree.add_vertex(
                name=node.pop("id", None), minima=node.pop("minima", None), attrs=node
            )
        if "links" in tree_data:
            edges = tree_data["links"]
            for edge in edges:
                self._tree.add_edge(
                    source=edge.pop("source", None),
                    target=edge.pop("target", None),
                    attrs=edge,
                )
        # self.__validate()

    def from_json(self, data_path: Union[str, Path]):
        tree_data = file_utils.read_json_tree(data_path)
        self.from_dict(tree_data=tree_data)

    def load_edge(self, edge_info: list):
        for edge in edge_info:
            self._tree.add_edge(source=edge["source"], target=edge["target"])

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
    def add_node(
        self, minima: float, link: Link = None, parent: Node = None, **kwargs
    ) -> int:
        if self._tree.vcount() == 0:
            self._tree.add_vertex(name=self.root_id, minima=0, link=None)
        node_id = self._tree.add_vertex(name=None, minima=minima)
        return node_id

    def add_edge(self) -> int:
        pass

    def structure(self) -> dict:
        pass

    # TODO: Check if this is necessary
    # def read_path(self, node_id: int):
    #     class SequenceInfo(NamedTuple):
    #         node_id: int
    #         minima: float
    #         axis: int
    #         direction: int
    #
    #     path_sequence = []
    #
    #     def get_parent(current_id: int):
    #         current_vertex = self._tree.vs[current_id]
    #         edge_info = current_vertex.in_edges()[0]
    #         up_link = Link(edge_info)
    #         path_sequence.append(
    #             SequenceInfo(
    #                 current_id,
    #                 Node(current_vertex).minima,
    #                 up_link.axis,
    #                 up_link.direction,
    #             )
    #         )
    #         return edge_info.source
    #
    #     current_node = self._tree.vs[node_id]
    #     if current_node.out_edges():
    #         # TODO: Change this to warning
    #         print("Not terminal node")
    #
    #     while node_id != 0:
    #         source_node = get_parent(node_id)
    #         node_id = source_node
    #
    #     path_sequence.append(
    #         SequenceInfo(self.root_node.node_id, self.root_node.minima, 0, 0)
    #     )
    #     return path_sequence

    def to_sequence(self) -> list:
        sequence_info = []
        for vertex in self._tree.vs:
            attrs = vertex.attributes()
            attrs["attrs"]["id"] = attrs["name"]
            attrs["attrs"]["minima"] = attrs["minima"]
            sequence_info.append(attrs)
        return sequence_info

    @property
    def dim_space(self) -> int:
        return self._tree["dim_space"]

    @property
    def root_id(self) -> int:
        return 0

    @property
    def root_minima(self) -> float:
        return 0.0

    @property
    def root_symbol(self) -> list:
        return []

    @property
    def root_node(self) -> Node:
        return Node(self._tree.vs[self.root_id])


if __name__ == "__main__":
    tree = Tree(dim_space=2)
    base_path = Path(__file__).parent.absolute().parents[2]
    data_path = base_path / "sample.json"
    tree.from_json(data_path)
    tree.to_sequence()
    print(tree)
    print(tree.to_sequence())
