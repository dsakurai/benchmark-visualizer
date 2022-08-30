import igraph

from custom_benchmark_problems.diamon_problem.data_structures.movement import Movement
from custom_benchmark_problems.diamon_problem.data_structures.node import Node


class Tree:
    def __init__(self, dim_space: int, **kwargs):
        kwargs["dim_space"] = dim_space
        # Create a directed graph with 0 vertex
        # https://igraph.org/python/api/latest/igraph.Graph.html#__init__
        self._tree = igraph.Graph(n=0, directed=True, graph_attrs=kwargs)

    def from_json(self):
        pass

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
