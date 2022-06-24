from networkx import Graph

from source import multimodal_benchmark
from utils import graph_utils


class ProblemConstructor:
    def __init__(self):
        pass

    @staticmethod
    def graph_to_problem_tree(graph: Graph, dim_space: int) -> multimodal_benchmark.Tree:
        tree = multimodal_benchmark.Tree(dim_space=dim_space)
        for vertex_id, vertex in graph.nodes(data=True):
            edges = graph_utils.find_edge(vertex_id=vertex_id, graph=graph)
            if edges is not None:
                for edge in edges:
                    src_vertex, tgt_vertex, payload = edge
                    # Do we have some kind of index or identifier for node??
                    tree.add_node(
                        parent=src_vertex,  # !!!!!!!!!!!! via igraph search
                        movement=multimodal_benchmark.Movement(
                            axis=0, direction=multimodal_benchmark.Movement.forward
                        ),
                        value_min=graph_utils.get_vertex_payload(tgt_vertex, graph)[
                            "minima"
                        ],
                    )
            else:
                raise Exception("Vertex cannot be floating around")
        return tree
