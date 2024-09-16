import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from jmetal.core.quality_indicator import GenerationalDistance
from jmetal.core.quality_indicator import InvertedGenerationalDistance
import os

class PerformanceEvaluator:
    def __init__(self):
        pass
    @staticmethod
    def gd(reference, actual):
        return GenerationalDistance(reference).compute(actual)
    @staticmethod
    def igd(reference, actual):
        return InvertedGenerationalDistance(reference).compute(actual)

    def match_experiment_file(self,
            data_base_path: str, solver: str, tree: str, dimension: int, termination: str
    ):
        file_name_pattern = f"{solver}_{tree}_{dimension}_{termination}"
        files = [
            f
            for f in os.listdir(data_base_path)
            if os.path.isfile(os.path.join(data_base_path, f))
        ]
        for file in files:
            if file.startswith(file_name_pattern):
                return os.path.join(data_base_path, file)

        # ファイルが見つからなかった場合のエラーメッセージ
        raise FileNotFoundError(
            f"No file found for pattern: {file_name_pattern} in {data_base_path}"
        )

    def compute_indicators(self,
            reference_set,
            reference_front,
            generation_set,
            generation_front,
            pareto_dict: dict,
            generation_points_node_x,
            generation_points_node_y,
            indicator_type,
    ):
        if indicator_type == "GD":
            indicator = self.gd
            indicator_str = "GD"
        elif indicator_type == "IGD":
            indicator = self.igd
            indicator_str = "IGD"
        else:
            raise NotImplementedError("Unrecognized Quality Indicator")

        # Generational Distanceの計算
        gd_value = indicator(reference=reference_front, actual=generation_front)
        gdx_value = indicator(reference=reference_set, actual=generation_set)

        global_indicators = {"gd": gd_value, "gdx": gdx_value}

        node_indicators = {}
        for node_id in pareto_dict.keys():
            # Generational Distanceの計算
            pareto_set = generation_points_node_x[generation_points_node_x[:, 3] == node_id, :][
                  :, 0:3
                  ]
            front = generation_points_node_y[generation_points_node_y[:, 2] == node_id, :][
                    :, 0:2
                    ]

            if front.size > 0:
                gd_value = indicator(
                    reference=pareto_dict[node_id]["pareto_front"], actual=front
                )
                gdx_value = indicator(
                    reference=pareto_dict[node_id]["pareto_set"], actual=pareto_set
                )
                # print(f"{indicator_str} for node[{node_id}]: ", gd_value)
                # print(f"{indicator_str} X for node[{node_id}]: ", gdx_value)
                node_indicators[node_id] = {"gd": gd_value, "gdx": gdx_value}
            else:
                # print(f"{indicator_str} for node[{node_id}]: NaN")
                node_indicators[node_id] = {"gd": None, "gdx": None}
                return {"global": global_indicators, "node": node_indicators}