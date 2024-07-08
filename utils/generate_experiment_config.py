import yaml


def compose_solver_settings(solver_name) -> dict:
    if solver_name == "GDE3":
        settings = {"population_size": 100, "cr": 0.5, "f": 0.5}
    elif solver_name == "NSGAII":
        settings = {
            "population_size": 100,
            "offspring_population_size": 100,
            "mutation": {
                "mutation": "PolynomialMutation",
                "probability": "n_variables",
                "distribution_index": 20,
            },
            "crossover": {
                "crossover": "SBXCrossover",
                "probability": 1.0,
                "distribution_index": 20,
            },
        }
    elif solver_name == "IBEA":
        settings = {
            "kappa": 1.0,
            "population_size": 100,
            "offspring_population_size": 100,
            "mutation": {
                "mutation": "PolynomialMutation",
                "probability": "n_variables",
                "distribution_index": 20,
            },
            "crossover": {
                "crossover": "SBXCrossover",
                "probability": 1.0,
                "distribution_index": 20,
            },
        }
    elif solver_name == "MOEAD":
        settings = {
            "population_size": 100,
            "mutation": {
                "mutation": "PolynomialMutation",
                "probability": "n_variables",
                "distribution_index": 20,
            },
            "crossover": {
                "crossover": "DifferentialEvolutionCrossover",
                "CR": 1.0,
                "F": 0.5,
                "K": 0.5,
            },
            "aggregative_function": {
                "aggregative_function": "Tschebycheff",
                "dimension": "n_variables",
            },
            "neighbor_size": 20,
            "neighbourhood_selection_probability": 0.9,
            "max_number_of_replaced_solutions": 2,
            "weight_files_path": "resources/MOEAD_weights",
        }
    elif solver_name == "OMOPSO":
        settings = {
            "swarm_size": 100,
            "epsilon": 0.0075,
            "uniform_mutation": {
                "uniform_mutation": "UniformMutation",
                "probability": "n_variables",
                "perturbation": 0.5,
            },
            "non_uniform_mutation": {
                "non_uniform_mutation": "NonUniformMutation",
                "probability": "n_variables",
                "perturbation": 0.5,
                "max_iterations": "max_evaluations/swarm_size",
            },
            "leaders": {"leaders": "CrowdingDistanceArchive", "maximum_size": 100},
        }
    else:
        raise NotImplementedError
    return settings


if __name__ == "__main__":
    exp_base_name = "test_exp"
    # trees = ["experiment_trees/diverse_tree.json"]
    # trees = []
    # depth_trees = [f"experiment_trees/depth_base_{i}.json" for i in range(1, 7)]
    # breadth_trees = [f"experiment_trees/breadth_base_{i}.json" for i in range(1, 7)]
    # trees.extend(breadth_trees)
    # trees.extend(depth_trees)
    trees = ["experiment_trees/depth_base_1.json"]
    solvers = ["GDE3", "NSGAII", "IBEA", "MOEAD"]
    dimensions = [5]
    termination_criterions = [
        # {"criterion_name": "StoppingByTime", "termination_parameter": 200},
        {"criterion_name": "StoppingByEvaluations", "termination_parameter": 100000},
    ]
    counter = 0
    exp_settings = []
    for tree in trees:
        for solver in solvers:
            for dimension in dimensions:
                for termination_criterion in termination_criterions:
                    exp_settings.append(
                        {
                            "experiment_name": exp_base_name + f"_v{counter}",
                            "tree_file": tree,
                            "dimension": dimension,
                            "algorithm": solver,
                            "algorithm_parameters": compose_solver_settings(solver),
                            "termination_criterion": dict(termination_criterion),
                        }
                    )
                    counter += 1
    with open("../exp_config_diverse.yaml", "w") as file:
        documents = yaml.safe_dump(exp_settings, file)
