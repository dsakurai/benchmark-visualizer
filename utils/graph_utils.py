import pickle

import networkx as nx
from networkx import Graph


def dict2graph(tree_info: dict) -> Graph:
    graph = nx.Graph()
    for vertex in tree_info["vertices"]:
        graph.add_nodes_from([(vertex["id"], vertex)])
    for edge in tree_info["edges"]:
        graph.add_edges_from([(edge["source"], edge["target"], edge)])
    return graph


def get_vertex_payload(vertex_id, graph: Graph):
    return graph.nodes[vertex_id]


def graph2dict(graph: Graph) -> dict:
    vertices = []
    edges = []
    for vertex_id, vertex in graph.nodes(data=True):
        vertices.append(vertex)
    for src_vertex, tgt_vertex, edge in graph.edges(data=True):
        edges.append(edge)
    return {"vertices": vertices, "edges": vertices}


def find_edge(vertex_id: int, graph: Graph) -> Graph.edges:
    return graph.edges(vertex_id, data=True)


def pickle_construction_tree(construction_tree: dict):
    return pickle.dumps(construction_tree, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    dict_info = {
        "vertices": [
            {"id": 0, "group": 0, "minima": -1},
            {"id": 1, "group": 0, "minima": 0},
            {"id": 2, "group": 0, "minima": 0},
            {"id": 3, "group": 0, "minima": 0},
            {"id": 4, "group": 0, "minima": 0},
            {"id": 5, "group": 0, "minima": 0},
            {"id": 6, "group": 0, "minima": 0},
            {"id": 7, "group": 0, "minima": 0},
        ],
        "edges": [
            {"source": 0, "target": 1, "value": 1},
            {"source": 0, "target": 2, "value": 1},
            {"source": 0, "target": 3, "value": 1},
            {
                "source": 1,
                "target": 0,
                "value": 1,
            },  # Bug test passed, but we'd leave it here
            {"source": 1, "target": 4, "value": 1},
            {"source": 1, "target": 5, "value": 1},
            {"source": 3, "target": 6, "value": 1},
            {"source": 3, "target": 7, "value": 1},
        ],
    }
    G = dict2graph(dict_info)
