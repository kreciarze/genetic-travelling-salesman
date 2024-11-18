# Python3 implementation of the above approach
from random import randint

from enum import Enum

from typing import Any, Callable
from matplotlib import pyplot as plt
import numpy as np

from travel_graph import euclidean_distance


type DistanceFunction = Callable[[Any, Any], float]


class Individual:
    def __init__(self) -> None:
        self.gnome: np.array = np.array([])
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return f"Individual(gnome: {self.gnome}, fitness: {round(self.fitness, 2)})"


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
        self.convergence_array = []

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

        r1 = TravelGraphClassic.rand_num(
            1, s.size-int(crossover_factor*s.size))
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

    def fitness_function(gnome, nodes, distance_function=euclidean_distance):

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
        population_size=1000,           # 1000
        generations=500,                # 500
        elitism_factor=0.15,            # 0.15
        elitism_factor_change=None,     # None
        diversity_factor=0.15,          # 0.15
        diversity_factor_change=None,   # None
        crossover_factor=0.1,           # 0.1
        crossover_factor_change=None,   # None
        p_mutation=0.01,                # 0.01
        p_mutation_change=None,         # None
        mutate_elite=True,              # True
        patience=50,                    # 50
        patience_factor=0.001,          # 0.001
        verbose=2,                      # 2
    ):
        i_generation = 1
        population = []

        # 1) Initialize the population
        for i in range(population_size):
            temp = Individual()
            temp.gnome = self.create_gnome()
            temp.fitness = TravelGraphClassic.fitness_function(
                temp.gnome, self.nodes, self.distance_function)
            population.append(temp)

        if verbose > 2:
            print("\nInitial population:")
            for i in range(population_size):
                print("\t", population[i])
            print()

        # 6) Evolution
        while i_generation <= generations:
            if verbose >= 1:
                params_dict = {
                    "elitism_factor": round(elitism_factor,4),
                    "diversity_factor": round(diversity_factor,4),
                    "crossover_factor": round(crossover_factor,4),
                    "p_mutation": round(p_mutation,4),
                }
                print(f"Generation {i_generation} ({params_dict})")

            new_population = []

            # 2) Selection
            population = sorted(population, key=lambda x: x.fitness)
            new_population.extend(
                population[:int(elitism_factor * population_size)])
            elite_count = len(new_population)

            # 5) Diversity
            for i in range(int(diversity_factor * population_size)):
                temp = Individual()
                temp.gnome = self.create_gnome()
                temp.fitness = TravelGraphClassic.fitness_function(
                    temp.gnome, self.nodes, self.distance_function)
                new_population.append(temp)
            elite_and_diversity_count = len(new_population)

            # 3) Crossovers
            while len(new_population) < population_size:
                p1 = population[TravelGraphClassic.rand_num(
                    0, elite_and_diversity_count)]
                p2 = population[TravelGraphClassic.rand_num(
                    0, elite_and_diversity_count)]

                if p1 != p2:
                    child = Individual()
                    child.gnome = TravelGraphClassic.crossover_genes_pmx(
                        p1.gnome, p2.gnome, crossover_factor)
                    child.fitness = TravelGraphClassic.fitness_function(
                        child.gnome, self.nodes, self.distance_function)
                    new_population.append(child)

            # 4) Mutations
            mutation_start_index = 0 if mutate_elite else elite_count
            for individual in new_population[mutation_start_index:]:
                individual.gnome = self.mutate_gene(
                    individual.gnome, p_mutation)
                individual.fitness = TravelGraphClassic.fitness_function(
                    individual.gnome, self.nodes, self.distance_function)

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
            self.convergence_array.append(sorted_population[0].fitness)
            self.current_solution = sorted_population[0].gnome
            self.current_fitness = sorted_population[0].fitness
            population = new_population
            i_generation += 1
            if elitism_factor_change is not None:
                elitism_factor += elitism_factor_change
            if diversity_factor_change is not None:
                diversity_factor += diversity_factor_change
            if crossover_factor_change is not None:
                crossover_factor += crossover_factor_change
            if p_mutation_change is not None:
                p_mutation += p_mutation_change

            if len(self.convergence_array)-patience > 0:
                recent_convergences = self.convergence_array[len(
                    self.convergence_array)-patience:]
                recent_convergences_change = abs(
                    recent_convergences[0] / recent_convergences[-1] - 1)
                if patience_factor is not None and recent_convergences_change < patience_factor:
                    if verbose >= 1:
                        print(f"Patience reached. Recent population change: {
                              recent_convergences_change}")
                    break

        if generations == i_generation:
            if verbose >= 1:
                print(f"Max generations reached: {generations}")

    def get_solution(self):
        return self.current_solution

    def get_fitness(self):
        return self.current_fitness

    def get_convergence(self):
        return self.convergence_array
