from typing import Any, Callable

import numpy as np
from pygad import GA

from ga_utils.distance_functions import DistanceFunction, distance_euclidean


class TravelGraphGA:
    def __init__(
        self,
        nodes: np.ndarray,
        distance_function: DistanceFunction = distance_euclidean,
    ) -> None:
        self.nodes = nodes
        self.distance_function = distance_function

    def find_shortest_path(self) -> tuple[list[int], float]:
        ga_instance = GA(
            num_generations=200,
            num_parents_mating=20,
            fitness_func=self.fitness_function,
            initial_population=self.generate_biased_population(
                population_size=100),
            num_genes=len(self.nodes),
            init_range_low=0,
            init_range_high=len(self.nodes) - 1,
            gene_type=int,
            parent_selection_type="tournament",
            keep_parents=1,
            keep_elitism=2,
            K_tournament=5,
            crossover_type="single_point",
            crossover_probability=0.8,
            mutation_type="random",
            mutation_probability=0.2,
            mutation_num_genes=max(round(len(self.nodes) * 0.1), 1),
            gene_space=[i for i in range(len(self.nodes))],
            allow_duplicate_genes=False,
            stop_criteria=[
                "saturate_10",
            ],
            random_seed=42,
        )
        ga_instance.run()

        solution, solution_fitness, _ = ga_instance.best_solution()
        distance = -solution_fitness
        return solution, distance

    def generate_biased_population(self, population_size: int, random_fraction: float = 0.2) -> list[np.ndarray]:
        base_order = np.arange(len(self.nodes))
        population = []

        num_random_individuals = int(population_size * random_fraction)
        num_biased_individuals = population_size - num_random_individuals

        for _ in range(num_biased_individuals):
            individual = base_order.copy()

            num_swaps = np.random.randint(2, 6)
            for _ in range(num_swaps):
                i, j = np.random.choice(len(self.nodes), size=2, replace=False)
                individual[i], individual[j] = individual[j], individual[i]

            population.append(individual)

        for _ in range(num_random_individuals):
            random_individual = np.random.permutation(base_order)
            population.append(random_individual)

        return population

    def fitness_function(self, ga_instance: GA, solution: np.ndarray, solution_idx: int) -> float:
        distance = 0.0
        solution_shift = np.roll(solution, -1)

        for node_1_id, node_2_id in zip(solution, solution_shift):
            distance += self.distance_function(
                self.nodes[node_1_id], self.nodes[node_2_id])

        return -distance
