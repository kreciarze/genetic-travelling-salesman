# Python3 implementation of the above approach
from random import randint

from enum import Enum

from typing import Any, Callable
from matplotlib import pyplot as plt
import numpy as np

import time
from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file

from plotter import plot_nodes_to_file
from travel_graph import TravelGraph
import os


type DistanceFunction = Callable[[Any, Any], float]


def euclidean_distance(node_1: np.ndarray, node_2: np.ndarray) -> float:
    return float(np.linalg.norm(node_1 - node_2))


class Individual:
    def __init__(self) -> None:
        self.gnome: np.array = np.array([])
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return f"Individual(gnome: {self.gnome}, fitness: {round(self.fitness,2)})"

class TravelGraphClassic:

    def __init__(
        self,
        nodes: np.ndarray,
        distance_function: DistanceFunction = euclidean_distance,
    ) -> None:
        self.nodes = nodes
        self.distance_function = distance_function
        self.V = len(nodes)
        self.current_solution = None
        self.current_fitness = float("inf")

    @staticmethod
    def rand_num(start, end):
        return randint(start, end-1)

    def create_gnome(self):
        gnome = [0]
        while True:
            if len(gnome) == self.V:
                gnome.append(gnome[0])
                break

            v = TravelGraphClassic.rand_num(0, self.V)
            if not v in gnome:
                gnome.append(v)

        return np.array(gnome)
    
    @staticmethod
    def crossover_genes_pmx(s, t, crossover_factor=0.1):
        # s, t - parents
        # c - child

        s = s.copy()
        t = t.copy()

        c = s.copy()

        r1 = TravelGraphClassic.rand_num(1, s.size-int(crossover_factor*s.size))
        r2 = r1 + max(1, int(crossover_factor*s.size))

        for i in range(r1, r2):
            j = np.where(s == t[i])[0][0]
            if i != 0 and j != 0:
                c[i], c[j] = c[j], c[i]

        return c

    def mutate_gene(self, gnome, p_mutation=0.007):
        gnome = gnome.copy()
        for i in range(1, len(gnome)):
            if np.random.rand() < p_mutation:
                while True:
                    j = TravelGraphClassic.rand_num(1, len(gnome)-1)
                    if i != j:
                        gnome[i], gnome[j] = gnome[j], gnome[i]
                        break
        return gnome

    def fitness_function(gnome, distance_function=euclidean_distance):

        f = 0
        for i in range(len(gnome) - 1):
            a = gnome[i]
            b = gnome[i + 1]

            node_a = nodes[a]
            node_b = nodes[b]

            f += distance_function(node_a, node_b)

        e = gnome[len(gnome) - 1]
        s = gnome[0]
        node_end = nodes[e]
        node_start = nodes[s]

        f += distance_function(node_end, node_start)

        return f

    def find_shortest_path(
        self,
        population_size=500, # 500
        generations=500, # 500
        elitism_factor=0.15, # 0.15
        diversity_factor=0.15, # 0.15
        linear_selection_factor=0.5, # 0.5
        crossover_factor=10/131, # 10/131
        p_mutation=0.01, # 0.01
        mutate_elite=True, # True
        patience=50, # 50
        patience_factor=0.001, # 0.001
        verbose=2, # 2
        convergence_array=None, # None
    ):
        i_generation = 1
        population = []

        # 1) Initialize the population
        for i in range(population_size):
            temp = Individual()
            temp.gnome = self.create_gnome()
            temp.fitness = TravelGraphClassic.fitness_function(temp.gnome, self.distance_function)
            population.append(temp)

        if verbose > 2:
            print("\nInitial population:")
            for i in range(population_size):
                print("\t", population[i])
            print()

        # 6) Evolution
        while i_generation <= generations:
            if verbose >= 1:
                print(f"Generation {i_generation}")

            new_population = []

            # 2) Selection
            population = sorted(population, key=lambda x: x.fitness)
            new_population.extend(population[:int(elitism_factor * population_size)])
            elite_count = len(new_population)

            # 5) Diversity
            for i in range(int(diversity_factor * population_size)):
                temp = Individual()
                temp.gnome = self.create_gnome()
                temp.fitness = TravelGraphClassic.fitness_function(temp.gnome, self.distance_function)
                new_population.append(temp)
            elite_and_diversity_count = len(new_population)

            # 3) Crossovers
            linear_selection_factor
            while len(new_population) < population_size:
                # p1 = population[TravelGraphClassic.rand_num(0, int(linear_selection_factor*len(population)))]
                # p2 = population[TravelGraphClassic.rand_num(0, int(linear_selection_factor*len(population)))]
                p1 = population[TravelGraphClassic.rand_num(0, elite_and_diversity_count)]
                p2 = population[TravelGraphClassic.rand_num(0, elite_and_diversity_count)]

                if p1 != p2:
                    child = Individual()
                    child.gnome = TravelGraphClassic.crossover_genes_pmx(p1.gnome, p2.gnome, crossover_factor)
                    child.fitness = TravelGraphClassic.fitness_function(child.gnome, self.distance_function)
                    new_population.append(child)

            # 4) Mutations
            mutation_start_index = 0 if mutate_elite else elite_count
            for individual in new_population[mutation_start_index:]:
                individual.gnome = self.mutate_gene(individual.gnome, p_mutation)
                individual.fitness = TravelGraphClassic.fitness_function(individual.gnome, self.distance_function)

            # Logging
            sorted_population = sorted(new_population, key=lambda x: x.fitness)
            if verbose >= 2:
                if verbose >= 3:
                    print("\nPopulation:")
                    for i in range(population_size):
                        print(f"\t{new_population[i]}")
                print(f"Population best: {sorted_population[0]}")
                print()

            # Prepare for the next generation
            convergence_array.append(sorted_population[0].fitness)
            self.current_solution = sorted_population[0].gnome
            self.current_fitness = sorted_population[0].fitness
            population = new_population
            i_generation += 1
            
            if len(convergence_array)-patience > 0:
                recent_convergences = convergence_array[len(convergence_array)-patience:]
                recent_convergences_change = abs(recent_convergences[0] / recent_convergences[-1] -1)
                if patience_factor is not None and recent_convergences_change < patience_factor:
                    if verbose >= 1:
                        print(f"Patience reached. Recent population change: {recent_convergences_change}")
                    break

        if generations == i_generation:
            if verbose >= 1:
                print(f"Max generations reached: {generations}")

        if verbose >= 1:
            print("\n\nLast fitness: ", self.current_fitness)

        return self.current_solution, self.current_fitness


if __name__ == "__main__":

    # problem_name = input("Enter the problem name [xqf131]: ")
    # problem_name = problem_name or "xqf131"
    # problem_name = "easy"
    problem_name = "bays29"
    # problem_name = "berlin52"
    # problem_name = "eli101"
    # problem_name = "xqf131"
    tsp_file_path = f"data/{problem_name}/{problem_name}.tsp"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)
    nodes = tsp_file.nodes
    plot_nodes_to_file(
        nodes=nodes,
        file_path=f"data/{problem_name}/{problem_name}.png",
        title=f"{problem_name} Nodes",
    )

    tour_file_path = f"data/{problem_name}/{problem_name}.tour"
    tour_file = parse_tour_file(file_path=tour_file_path)
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path=f"data/{problem_name}/{problem_name}_tour.png",
        title=f"{problem_name} Tour",
        order=tour_file.tour,
    )

    distance_function=euclidean_distance
    weights_file_path = f"data/{problem_name}/{problem_name}.weights"
    if os.path.exists(weights_file_path):
        print("Using weights file")
        weights = np.loadtxt(weights_file_path)
        nodes = [i for i in range(len(nodes))]

        weights_distance_function = np.vectorize(lambda node_1, node_2: weights[node_1, node_2])
        distance_function = weights_distance_function


    convergence_array = []

    travel_graph = TravelGraphClassic(
        nodes=nodes,
        distance_function = distance_function,
    )
    start_time = time.perf_counter()
    try:
        travel_graph.find_shortest_path(
            convergence_array=convergence_array,
        )
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by the user.")
    end_time = time.perf_counter()

    solution, distance = travel_graph.current_solution, travel_graph.current_fitness

    print(f"Time elapsed: {end_time - start_time:.2f} seconds")
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path=f"data/{problem_name}/{problem_name}_solution.png",
        title=f"{problem_name} Solution",
        order=solution,
    )

    plt.plot(convergence_array)
    plt.title(f"{problem_name} convergence")
    plt.xlabel("Generation")
    plt.ylabel("Distance")
    plt.tight_layout(pad=1)
    plt.savefig(f"data/{problem_name}/{problem_name}_convergence.png", format="png", dpi=100)
    
