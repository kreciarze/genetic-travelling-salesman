from typing import Callable
import numpy as np


type CrossoverFunction = Callable[[
    np.ndarray, np.ndarray, float], np.ndarray]


def crossover_genes_pmx(s, t, crossover_factor=0.1):
    # s, t - parents
    # c - child

    s = s.copy()
    t = t.copy()

    c = s.copy()

    r1 = np.random.randint(
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
