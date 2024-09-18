import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from jmetal.core.quality_indicator import GenerationalDistance
from jmetal.core.quality_indicator import InvertedGenerationalDistance
from jmetal.core.quality_indicator import HyperVolume
import os

from utils.file_utils import parse_exp_log_dir, load_n_evaluation_log
from utils.reference_fronts import ReferenceFronts


class PerformanceEvaluator:
    def __init__(self):
        pass

    @staticmethod
    def gd(reference, actual):
        return GenerationalDistance(reference).compute(actual)

    @staticmethod
    def igd(reference, actual):
        return InvertedGenerationalDistance(reference).compute(actual)

    @staticmethod
    def hv(reference, actual):
        return HyperVolume(reference).compute(actual)

    @staticmethod
    def match_experiment_file(
        data_base_path: str,
        solver: str,
        tree: str,
        dimension: int,
        termination: str,
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

    def compute_indicator(
        self,
        reference_set,
        reference_front,
        actual_set,
        actual_front,
        indicator_type: str,
    ):
        if indicator_type == "GD":
            indicator = self.gd
            indicator_str = "GD"
        elif indicator_type == "IGD":
            indicator = self.igd
            indicator_str = "IGD"
        elif indicator_type == "HV":
            raise NotImplementedError(
                "HyperVolume requires a reference point and therefore is not implemented yet @240918"
            )
            indicator = self.hv
            indicator_str = "HyperVolume"
        else:
            raise NotImplementedError("Unrecognized Quality Indicator")

        return {
            "set_indicator": indicator(reference_set, actual_set),
            "front_indicator": indicator(reference_front, actual_front),
        }

    # def compute_indicators(
    #     self,
    #     reference_set,
    #     reference_front,
    #     generation_set,
    #     generation_front,
    #     pareto_dict: dict,
    #     generation_points_node_x,
    #     generation_points_node_y,
    #     indicator_type,
    # ):
    #     if indicator_type == "GD":
    #         indicator = self.gd
    #         indicator_str = "GD"
    #     elif indicator_type == "IGD":
    #         indicator = self.igd
    #         indicator_str = "IGD"
    #     elif indicator_type == "HV":
    #         indicator = self.hv
    #         indicator_str = "HyperVolume"
    #     else:
    #         raise NotImplementedError("Unrecognized Quality Indicator")
    #
    #     gd_value = indicator(reference=reference_front, actual=generation_front)
    #     gdx_value = indicator(reference=reference_set, actual=generation_set)
    #
    #     global_indicators = {"gd": gd_value, "gdx": gdx_value}
    #
    #     node_indicators = {}
    #     for node_id in pareto_dict.keys():
    #         # Generational Distanceの計算
    #         pareto_set = generation_points_node_x[
    #             generation_points_node_x[:, 3] == node_id, :
    #         ][:, 0:3]
    #         front = generation_points_node_y[
    #             generation_points_node_y[:, 2] == node_id, :
    #         ][:, 0:2]
    #
    #         if front.size > 0:
    #             gd_value = indicator(
    #                 reference=pareto_dict[node_id]["pareto_front"], actual=front
    #             )
    #             gdx_value = indicator(
    #                 reference=pareto_dict[node_id]["pareto_set"], actual=pareto_set
    #             )
    #             # print(f"{indicator_str} for node[{node_id}]: ", gd_value)
    #             # print(f"{indicator_str} X for node[{node_id}]: ", gdx_value)
    #             node_indicators[node_id] = {"gd": gd_value, "gdx": gdx_value}
    #         else:
    #             # print(f"{indicator_str} for node[{node_id}]: NaN")
    #             node_indicators[node_id] = {"gd": None, "gdx": None}
    #             return {"global": global_indicators, "node": node_indicators}


def main():
    pe = PerformanceEvaluator()
    exp_dir = "../data/N-obj-test_v13"
    exp_info = parse_exp_log_dir(exp_dir=exp_dir)
    meta = exp_info["meta"]
    dimension = meta["dimension"]
    n_objectives = meta["n_objectives"]
    log_df = load_n_evaluation_log(file_path=exp_info["result"], return_df=True)
    n_ts = n_objectives - 1
    n_xs = dimension
    design_variable_header = [f"t{t+1}" for t in range(n_ts)] + [
        f"x{x+1}" for x in range(n_xs)
    ]
    objective_value_header = [f"y{y+1}" for y in range(n_objectives)]
    rf = ReferenceFronts()
    res = rf.get_n_obj_local_pareto_set(
        dimension=dimension,
        tree_file_path=exp_info["tree"],
        resolution=10,
        n_objectives=n_objectives,
    )
    start_step = 0
    end_step = start_step + meta["algorithm_parameters"]["population_size"]
    design_variables = log_df[start_step:end_step][design_variable_header].values
    objective_values = log_df[start_step:end_step][objective_value_header].values
    print(
        pe.compute_indicator(
            reference_set=res["all_sets"],
            reference_front=res["all_fronts"],
            actual_set=design_variables,
            actual_front=objective_values,
            indicator_type="HV",
        )
    )


if __name__ == "__main__":
    main()
