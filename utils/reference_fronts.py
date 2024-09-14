import os
from typing import Union

import numpy as np

from custom_benchmark_problems.diamon_problem.core import algs
from custom_benchmark_problems.diamon_problem.core import evaluation
from custom_benchmark_problems.diamon_problem.data_structures.tree import Tree


class ReferenceFronts:
    """This class is for compute the actual Pareto front (in theory)"""

    def __init__(self):
        pass

    def sampling_domain_axis(self):
        pass

    def get_local_pareto_set(
        self, dimension: int, tree_name: str, resolution: int = 100
    ):
        tree = Tree(dim_space=dimension)
        tree.from_json(f"../experiment_trees/{tree_name}.json")
        sequence_info = tree.to_sequence()
        bmp = evaluation.BMP(sequence_info=sequence_info, dim_space=dimension)
        pareto_dict = {}

        def apply_computing(data: np.array):
            row_data = bmp.evaluate(data)
            return np.array(
                [
                    row_data.t,
                    row_data.y,
                    # row_data.unrotated_value[0],
                    # row_data.unrotated_value[1],
                ]
            )

        all_sets = []
        all_fronts = []
        for node in sequence_info:
            node_id = node["name"]
            symbols = node["attrs"]["symbol"]
            minimum = node["minima"]
            central_coordinates = bmp.compute_coordinates(symbol_sequence=symbols)
            minimal_time = len(symbols) + 1

            # Compute unrotated value
            step_back = bmp.evaluate(
                np.insert(central_coordinates, 0, minimal_time - 1)
            )
            unrotated_y = step_back.unrotated_value[1]
            if minimum - unrotated_y <= -1:
                appearing_time = minimal_time
            else:
                appearing_time = minimal_time - 1

            t = np.linspace(appearing_time, bmp.t_upper_bound(), resolution)
            central_coordinates = np.broadcast_to(
                central_coordinates, (resolution, len(central_coordinates))
            )
            pareto_set = np.insert(central_coordinates, 0, t, axis=1)
            pareto_front = np.apply_along_axis(apply_computing, axis=1, arr=pareto_set)
            pareto_dict[node_id] = {
                "pareto_set": pareto_set,
                "pareto_front": pareto_front,
            }

            all_sets.append(pareto_set)
            all_fronts.append(pareto_front)
        # pareto_set_all = [pareto_dict[i]["pareto_set"] for i in range(len(pareto_dict))]
        # pareto_front_all = [pareto_dict[i]["pareto_front"] for i in range(len(pareto_dict))]
        all_sets = np.concatenate(all_sets, axis=0)
        all_fronts = np.concatenate(all_fronts, axis=0)
        return pareto_dict, all_sets, all_fronts
        # for node_id in pareto_dict.keys():
        #     pareto_set = pareto_dict[node_id]["pareto_set"]
        #     pareto_front = pareto_dict[node_id]["pareto_front"]


if __name__ == "__main__":
    rf = ReferenceFronts()
    res = rf.get_local_pareto_set(dimension=2, tree_name="breadth", resolution=10)
    print(res[0])
