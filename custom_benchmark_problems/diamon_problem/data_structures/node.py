import igraph


class Node:
    def __init__(self, vertex: igraph.Vertex, parent: int = None):
        self._vertex = vertex
        self._parent = parent

    def __eq__(self, other: "Node") -> bool:
        return self.index == other.index

    @property
    def index(self) -> int:
        return self._vertex.index

    @property
    def parent(self):
        return self.parent

    @property
    def node_id(self) -> int:
        return self._vertex["name"]

    @property
    def minima(self) -> float:
        return self._vertex["attrs"]["minima"]

    @property
    def sequence(self):
        return self._vertex["attrs"]["sequence"]
