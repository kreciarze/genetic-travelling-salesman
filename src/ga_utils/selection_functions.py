
from itertools import accumulate
from typing import Any, Callable
import numpy as np

class Selection:

    def __init__(self, selection_factor=0.1, selection_factor_change=None):
        self.selection_factor = selection_factor
        self.selection_factor_change = selection_factor_change

    def select(self, population: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def update(self):
        if self.selection_factor_change != None:
            self.selection_factor += self.selection_factor_change
            
class SelectionElitism(Selection):
    def __init__(
            self,
            selection_factor: int = .1,
            selection_factor_change = None
        ):
        super().__init__(selection_factor, selection_factor_change)

    def select(self, population: np.ndarray) -> np.ndarray:
        num_selections = int(len(population) * self.selection_factor)
        return sorted(population, key=lambda x: x.fitness)[:num_selections]

class SelectionTournament(Selection):
    def __init__(
            self,
            selection_factor: int = .1,
            selection_factor_change = None,
            tournament_factor: int = .4, 
            selection_p = .75
        ):
        super().__init__(selection_factor, selection_factor_change)
        self.tournament_factor = tournament_factor
        self.selection_p = selection_p

    def select(self,population: np.ndarray) -> np.ndarray:
        num_selections = int(len(population) * self.selection_factor)
        selected_individuals = []
        for _ in range(num_selections):
            tournament_size = int(len(population) * self.tournament_factor)
            tournament = np.random.choice(population, tournament_size, replace=False)
            tournament = sorted(tournament, key=lambda x: x.fitness, reverse=False)
            index = 0
            while np.random.random() < self.selection_p and index < len(tournament):
                index += 1
            if index == len(tournament):
                index = 0
            selected_individuals.append(tournament[index])
        return selected_individuals


class SelectionRouletteWheel(Selection):
    def __init__(
            self,
            selection_factor: int = .1,
            selection_factor_change = None
        ):
        super().__init__(selection_factor, selection_factor_change)
        

    def select(self, population: np.ndarray) -> np.ndarray:

        num_selections = int(len(population) * self.selection_factor)
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
