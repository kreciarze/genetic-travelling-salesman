# Python3 implementation of the above approach
from random import randint

from enum import Enum

from typing import Any, Callable
from matplotlib import pyplot as plt
from itertools import accumulate
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
    def selection_elitism(population, num_selections):
        return sorted(population, key=lambda x: x.fitness)[:num_selections]

    @staticmethod
    def selection_roulette_wheel(population, num_selections):
        # Step 1: Calculate Total Fitness
        total_fitness = sum(individual.fitness for individual in population)
        if total_fitness == 0:  # Handle edge case
            relative_fitness = [1 / len(population)] * len(population)  # Equal probabilities
        else:
            relative_fitness = [individual.fitness / total_fitness for individual in population]

        # Step 2: Build Cumulative Distribution
        cumulative_probabilities = list(accumulate(relative_fitness))

        # Step 3: Select Individuals
        selected_individuals = []
        for _ in range(num_selections):
            spin = np.random.random()  # Random number between 0 and 1
            for i, cumulative_prob in enumerate(cumulative_probabilities):
                if spin <= cumulative_prob:
                    selected_individuals.append(population[i])
                    break

        return selected_individuals


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


    def crossover_genes_edge_recombination(parent1, parent2, crossover_factor=None):
        parent1 = parent1.copy()
        parent2 = parent2.copy()

        # Step 1: Build Edge Table
        def build_edge_table(p1, p2):
            edge_table = {city: set() for city in p1}
            for p in (p1, p2):
                for i in range(len(p)):
                    city = p[i]
                    left = p[i - 1]  # Neighbor to the left
                    right = p[(i + 1) % len(p)]  # Neighbor to the right
                    edge_table[city].update([left, right])
            return edge_table

        # Step 2: Select the next city
        def select_next_city(current_city, edge_table):
            neighbors = edge_table.get(current_city)
            if neighbors is None or len(neighbors) == 0:
                # Pick random city if no neighbors
                while True:
                    next_city = np.random.choice(list(edge_table.keys()))
                    if next_city not in offspring:
                        return next_city
            
            # Choose city with the fewest neighbors
            next_city = min(neighbors, key=lambda x: len(edge_table[x]))
            return next_city

        # Initialize
        edge_table = build_edge_table(parent1, parent2)
        start_city = parent1[0]
        offspring = [start_city]
        current_city = start_city

        # Step 3: Build the offspring
        while len(offspring) < len(parent1)-1:
            # Remove current city from all neighbor lists
            for neighbors in edge_table.values():
                neighbors.discard(current_city)

            # Choose the next city
            next_city = select_next_city(current_city, edge_table)
            offspring.append(next_city)
            del edge_table[current_city]  # Remove current city from edge table
            current_city = next_city

        return np.array(offspring + [offspring[0]])


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

    def mutate_gene_displacement(self, solution, p_mutation=0.07):

        if np.random.rand() > p_mutation:
            return solution

        # Step 1: Select a subset
        n = len(solution)
        start = np.random.randint(1, n - 2)  # Ensure at least two elements remain for mutation
        end = np.random.randint(start + 1, n - 1)
        subset = solution[start:end + 1]

        # Step 2: Remove the subset
        remaining = np.concatenate((solution[:start], solution[end + 1:]))

        # Step 3: Reinsert the subset
        insert_pos = np.random.randint(1, len(remaining))  # Position in the remaining list
        mutated_solution = np.concatenate((remaining[:insert_pos], subset, remaining[insert_pos:]))

        return mutated_solution

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
                TravelGraphClassic.selection_elitism(
                    population, int(elitism_factor * population_size)
                )
                # TravelGraphClassic.selection_roulette_wheel(
                #     population, int(elitism_factor * population_size)
                # )
            )
            elite_count = len(new_population)

            # 5) Diversity
            for i in range(int(diversity_factor * population_size)):
                temp = Individual()
                temp.gnome = self.create_gnome()
                temp.fitness = TravelGraphClassic.fitness_function(
                    temp.gnome, self.nodes, self.distance_function)
                new_population.append(temp)
            # new_population.extend(
            #     TravelGraphClassic.selection_roulette_wheel(
            #         population, int(diversity_factor * population_size)
            #     )
            # )
            elite_and_diversity_count = len(new_population)

            # 3) Crossovers
            while len(new_population) < population_size:
                p1 = new_population[TravelGraphClassic.rand_num(
                    0, elite_and_diversity_count)]
                p2 = new_population[TravelGraphClassic.rand_num(
                    0, elite_and_diversity_count)]

                if p1 != p2:
                    child = Individual()
                    child.gnome = TravelGraphClassic.crossover_genes_edge_recombination(
                        p1.gnome, p2.gnome, crossover_factor)
                    child.fitness = TravelGraphClassic.fitness_function(
                        child.gnome, self.nodes, self.distance_function)
                    new_population.append(child)

            # 4) Mutations
            mutation_start_index = 0 if mutate_elite else elite_count
            for individual in new_population[mutation_start_index:]:
                individual.gnome = self.mutate_gene_displacement(
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
