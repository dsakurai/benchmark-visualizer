from networkx import Graph
from reeb_based_benchmark import multimodal_benchmark

from utils import graph_utils


class ProblemConstructor:
    def __init__(self):
        pass

    @staticmethod
    def graph_to_problem_tree(
        graph: Graph, dim_space: int
    ) -> multimodal_benchmark.Tree:
        tree = multimodal_benchmark.Tree(dim_space=dim_space)
        for vertex_id, vertex in graph.nodes(data=True):
            edges = graph_utils.find_edge(vertex_id=vertex_id, graph=graph)
            if edges is not None:
                for edge in edges:
                    src_vertex, tgt_vertex, payload = edge
                    if src_vertex == 0:
                        parent = tree.root_node
                    else:
                        parent = tree.find_node(graph.nodes[src_vertex]["igraph_index"])
                    node = tree.add_node(
                        parent=parent,
                        # TODO: Confirm how do we get this axis
                        movement=multimodal_benchmark.Movement(
                            axis=0, direction=multimodal_benchmark.Movement.forward
                        ),
                        value_min=graph_utils.get_vertex_payload(tgt_vertex, graph)[
                            "minima"
                        ],
                    )
                    graph.nodes[tgt_vertex]["igraph_index"] = node.index
            else:
                raise Exception("Vertex cannot be floating around")
        return tree
