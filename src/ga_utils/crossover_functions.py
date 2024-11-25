from typing import Callable
import numpy as np

class Crossover:
    
        def __init__(
                self, 
                crossover_factor=0.1, 
                crossover_factor_change=None
            ):
            self.crossover_factor = crossover_factor
            self.crossover_factor_change = crossover_factor_change

        def __call__(self, *args, **kwds):
            return self.crossover(*args, **kwds)
    
        def crossover(self, *args, **kwds):
            raise NotImplementedError()
    
        def update(self):
            if self.crossover_factor_change != None:
                self.crossover_factor += self.crossover_factor_change

class CrossoverGenesPMX(Crossover):

    def __init__(
            self, 
            crossover_factor=None,
            crossover_factor_change=None,
            use_factor_as_range=False,
        ):
        super().__init__(crossover_factor, crossover_factor_change)
        self.use_factor_as_range = use_factor_as_range

    def crossover(self, s, t):
        # s, t - parents
        # c - child

        s = s.copy()
        t = t.copy()

        c = s.copy()

        crossover_factor = self.crossover_factor
        if self.crossover_factor == None:
            crossover_factor = np.random.rand() * 0.9
        if self.use_factor_as_range:
            crossover_factor = np.random.random() * self.crossover_factor

        r1 = np.random.randint(
            1, s.size-int(crossover_factor*s.size))
        r2 = r1 + max(1, int(crossover_factor*s.size))

        for i in range(r1, r2):
            j = np.where(s == t[i])[0][0]
            if i != 0 and j != 0:
                c[i], c[j] = c[j], c[i]

        return c


class CrossoverGenesEdgeRecombination(Crossover):

    def __init__(
            self
        ):
        super().__init__(None, None)
        

    def build_edge_table(self, p1, p2):
        edge_table = {city: set() for city in p1}
        for p in (p1, p2):
            for i in range(len(p)):
                city = p[i]
                left = p[i - 1]  # Neighbor to the left
                right = p[(i + 1) % len(p)]  # Neighbor to the right
                edge_table[city].update([left, right])
        return edge_table

    def select_next_city(self, current_city, edge_table, offspring):
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

    def crossover(self, parent1, parent2):
        parent1 = parent1.copy()
        parent2 = parent2.copy()

        # Initialize
        edge_table = self.build_edge_table(parent1, parent2)
        start_city = parent1[0]
        offspring = [start_city]
        current_city = start_city

        # Step 3: Build the offspring
        while len(offspring) < len(parent1) - 1:
            # Remove current city from all neighbor lists
            for neighbors in edge_table.values():
                neighbors.discard(current_city)

            # Choose the next city
            next_city = self.select_next_city(current_city, edge_table, offspring)
            offspring.append(next_city)
            del edge_table[current_city]  # Remove current city from edge table
            current_city = next_city

        return np.array(offspring + [offspring[0]])