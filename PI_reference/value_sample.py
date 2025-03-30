def sample_func():
    tree = Tree(dim_space=2)
    tree.from_json("experiment_trees/sample.json")
    sequence_info = tree.to_sequence()
    bmp = evaluation.BMP(sequence_info=sequence_info, dim_space=2)

    symbols = [1]
    central_coordinates = bmp.compute_coordinates(symbol_sequence=symbols)
    minimal_time = len(symbols) + 1
    # (x1, x2): (2,2) ->
    # (t, x1, x2): (1, 2, 2)
    step_back = bmp.evaluate(np.insert(central_coordinates, 0, minimal_time - 1))

    rotated_t = step_back.t
    rotated_y = step_back.y

    unrotated_t = step_back.unrotated_value[0]
    unrotated_y = step_back.unrotated_value[1]
