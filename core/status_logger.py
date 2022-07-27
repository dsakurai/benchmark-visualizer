import numpy as np
from matplotlib import pyplot as plt


class StatusLogger:
    def __init__(self):
        self.solution_list = []
        self.variable_list = []

    def log_solution_status(self, solution_value):
        self.solution_list.append(solution_value)

    def log_variable_status(self, variable_value):
        self.variable_list.append(variable_value)

    def plot_solution(self):
        np_arr = np.array(self.solution_list)
        plot_arr = np_arr[0::100, 0]
        plt.scatter(range(plot_arr.shape[0]), plot_arr, marker=".")
        plt.xlabel("Evaluations")
        plt.ylabel("Solutions")
        print(plot_arr)
        plt.show()

    def plot_variable(self):
        np_arr = np.array(self.variable_list)
        print(np_arr.shape)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(np_arr[0::100, 0], np_arr[0::100, 1], range(np_arr[0::100, 1].shape[0]), marker=".")
        ax.set_xlabel('Variable 01')
        ax.set_ylabel('Variable 02')
        ax.set_zlabel('Evaluations')
        plt.show()
