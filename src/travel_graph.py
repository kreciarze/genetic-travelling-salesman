from typing import Any, Callable

import numpy as np
from pygad import GA

type DistanceFunction = Callable[[Any, Any], float]


def euclidean_distance(node_1: np.ndarray, node_2: np.ndarray) -> float:
    return float(np.linalg.norm(node_1 - node_2))


class TravelGraph:
    def __init__(
        self,
        nodes: np.ndarray,
        distance_function: DistanceFunction = euclidean_distance,
    ) -> None:
        self.nodes = nodes
        self.distance_function = distance_function

    def find_shortest_path(self) -> tuple[list[int], float]:
        ga_instance = GA(
            num_generations=100,
            num_parents_mating=4,
            fitness_func=self.fitness_function,
            sol_per_pop=300,
            num_genes=len(self.nodes),
            init_range_low=0,
            init_range_high=len(self.nodes) - 1,
            gene_type=int,
            parent_selection_type="sss",
            keep_parents=1,
            crossover_type="single_point",
            mutation_type="random",
            mutation_num_genes=max(round(len(self.nodes) * 0.05), 1),
            gene_space=[i for i in range(len(self.nodes))],
            allow_duplicate_genes=False,
        )
        ga_instance.run()

        solution, solution_fitness, _ = ga_instance.best_solution()
        distance = -solution_fitness
        return solution, distance

    def fitness_function(self, ga_instance: GA, solution: np.ndarray, solution_idx: int) -> float:
        distance = 0.0
        solution_shift = np.roll(solution, -1)

        for node_1_id, node_2_id in zip(solution, solution_shift):
            distance += self.distance_function(self.nodes[node_1_id], self.nodes[node_2_id])

        return -distance
