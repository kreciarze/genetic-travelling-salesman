from typing import Callable, List
import numpy as np

from ga_utils.individual import Individual
from ga_utils.selection_functions import SelectionRouletteWheel

type DiversificationFunction = Callable[[
    List[Individual], int, int, Callable], List[Individual]]


def diversification_random(population, num_selections, V, fitness_function):
    new_population = []
    for _ in range(num_selections):
        temp = Individual(V)
        temp.fitness = fitness_function(temp.gnome)
        new_population.append(temp)
    return new_population


@staticmethod
def diversification_roulette_wheel(population, num_selections, V, fitness_function):
    selection = SelectionRouletteWheel()
    return selection.select(
        population, num_selections
    )
