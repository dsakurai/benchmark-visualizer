import igraph


class Edge:
    def __init__(self, edge: igraph.Edge):
        self._edge = edge

    def __eq__(self, other: "Edge"):
        pass
