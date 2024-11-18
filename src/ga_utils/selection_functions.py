
from itertools import accumulate
from typing import Any, Callable
import numpy as np


type SelectionFunction = Callable[[np.ndarray, int], np.ndarray]


def selection_elitism(population: np.ndarray, num_selections: int) -> np.ndarray:
    return sorted(population, key=lambda x: x.fitness)[:num_selections]


def selection_roulette_wheel(population: np.ndarray, num_selections: int) -> np.ndarray:
    # Step 1: Calculate Total Fitness
    total_fitness = sum(individual.fitness for individual in population)
    if total_fitness == 0:  # Handle edge case
        # Equal probabilities
        relative_fitness = [1 / len(population)] * len(population)
    else:
        relative_fitness = [individual.fitness /
                            total_fitness for individual in population]

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
