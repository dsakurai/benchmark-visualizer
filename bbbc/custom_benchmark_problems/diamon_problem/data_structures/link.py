import igraph


class Link:
    def __init__(self, edge: igraph.Edge):
        self._edge = edge

    @property
    def source(self) -> int:
        return self._edge.source

    @property
    def target(self) -> int:
        return self._edge.target

    @property
    def direction(self) -> int:
        return self._edge["attrs"]["direction"]

    @property
    def axis(self) -> int:
        return self._edge["attrs"]["axis"]
