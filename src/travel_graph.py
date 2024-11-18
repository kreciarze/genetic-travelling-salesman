import numpy as np

from ga_utils.individual import Individual
from ga_utils.crossover_functions import CrossoverFunction, crossover_genes_pmx
from ga_utils.diversification_functions import DiversificationFunction, diversification_random
from ga_utils.mutation_functions import MutationFunction, mutate_gene_per_city
from ga_utils.selection_functions import SelectionFunction, selection_elitism
from ga_utils.distance_functions import DistanceFunction, distance_euclidean
from ga_utils.fintess_functions import FitnessFunction, fitness_classic


class TravelGraph:

    def __init__(
        self,
        nodes: np.ndarray,
        distance_function: DistanceFunction = distance_euclidean,
        fitness_function: FitnessFunction = fitness_classic,
        selection_function: SelectionFunction = selection_elitism,
        diversification_function: DiversificationFunction = diversification_random,
        crossover_genes_function: CrossoverFunction = crossover_genes_pmx,
        mutate_gene_function: MutationFunction = mutate_gene_per_city,
        
    ) -> None:
        self.nodes = nodes
        self.V = len(nodes)
        self.current_solution = None
        self.current_fitness = float("inf")
        self.convergence_array = []

        self.distance_function = distance_function
        self.fitness_function = fitness_function
        self.selection_function = selection_function
        self.diversification_function = diversification_function
        self.crossover_genes_function = crossover_genes_function
        self.mutate_gene_function = mutate_gene_function


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
            temp = Individual(self.V)
            temp.fitness = self.fitness_function(
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
                    "elitism_factor": round(elitism_factor, 4),
                    "diversity_factor": round(diversity_factor, 4),
                    "crossover_factor": round(crossover_factor, 4),
                    "p_mutation": round(p_mutation, 4),
                }
                print(f"Generation {i_generation} ({params_dict})")

            new_population = []

            # 2) Selection
            new_population.extend(
                self.selection_function(
                    population, int(elitism_factor * population_size)
                )
            )
            elite_count = len(new_population)

            # 5) Diversity
            new_population.extend(
                self.diversification_function(
                    population,
                    int(diversity_factor * population_size),
                    self.V,
                    fitness_function=lambda x: self.fitness_function(
                        x, self.nodes, self.distance_function)
                )
            )
            elite_and_diversity_count = len(new_population)

            # 3) Crossovers
            while len(new_population) < population_size:
                p1 = new_population[np.random.randint(
                    0, elite_and_diversity_count)]
                p2 = new_population[np.random.randint(
                    0, elite_and_diversity_count)]

                if p1 != p2:
                    child = Individual()
                    child.gnome = self.crossover_genes_function(
                        p1.gnome, p2.gnome, crossover_factor)
                    child.fitness = self.fitness_function(
                        child.gnome, self.nodes, self.distance_function)
                    new_population.append(child)

            # 4) Mutations
            mutation_start_index = 0 if mutate_elite else elite_count
            for individual in new_population[mutation_start_index:]:
                individual.gnome = self.mutate_gene_function(
                    individual.gnome, p_mutation)
                individual.fitness = self.fitness_function(
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
