from typing import NamedTuple, Dict, Any


class ExperimentSettings(NamedTuple):
    experiment_name: str
    tree_file: str
    dimension: int
    algorithm: str
    algorithm_parameters: Dict[str, Any]
    termination_criterion: Dict[str, Any]
