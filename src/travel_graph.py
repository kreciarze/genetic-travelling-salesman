import numpy as np
from pygad import GA


class TravelGraph:
    def __init__(self, city_names: list[str], distance_matrix: list[list[float]]) -> None:
        self.cities = city_names
        self.distance_matrix = distance_matrix

    def find_shortest_path(self) -> tuple[list[str], float]:
        ga_instance = GA(
            num_generations=50,
            num_parents_mating=2,
            fitness_func=self.fitness_function,
            sol_per_pop=50,
            num_genes=len(self.cities),
            init_range_low=0,
            init_range_high=len(self.cities) - 1,
            gene_type=int,
            parent_selection_type="sss",
            keep_parents=1,
            crossover_type="single_point",
            mutation_type="random",
            mutation_percent_genes=10,
            gene_space=[i for i in range(len(self.cities))],
            allow_duplicate_genes=False,
        )
        ga_instance.run()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        solution = self.ensure_start_from_first_city(solution)
        solution_cities = [self.cities[i] for i in solution]
        distance = -solution_fitness
        return solution_cities, distance

    def fitness_function(self, ga_instance: GA, solution: np.ndarray, solution_idx: int) -> float:
        distance = 0.0
        solution_shift = np.roll(solution, -1)

        for city_1, city_2 in zip(solution, solution_shift):
            distance += self.distance_matrix[city_1][city_2]

        return -distance

    @staticmethod
    def ensure_start_from_first_city(solution: np.ndarray) -> np.ndarray:
        first_city_idx = np.where(solution == 0)[0][0]
        solution_rolled = np.roll(solution, -first_city_idx)
        return solution_rolled
