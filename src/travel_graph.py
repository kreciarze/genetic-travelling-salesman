from random import random

import numpy as np
from pygad import GA


class TravelGraph:
    def __init__(self, city_names: list[str]) -> None:
        self.cities = city_names
        self.distance_matrix = []

        for city_1 in self.cities:
            city_1_distances = []

            for city_2 in self.cities:
                if city_1 == city_2:
                    city_1_distances.append(0.0)
                else:
                    city_1_distances.append(random())

            self.distance_matrix.append(city_1_distances)

    def fitness_function(self, ga_instance: GA, solution: np.ndarray, solution_idx: int) -> float:
        distance = 0.0
        solution_shift = np.roll(solution, -1)

        for city_1, city_2 in zip(solution, solution_shift):
            distance += self.distance_matrix[city_1][city_2]

        return -distance
