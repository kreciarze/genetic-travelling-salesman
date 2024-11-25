from typing import Any, Callable
import numpy as np

type MutationFunction = Callable[[np.ndarray, float], np.ndarray]

class Mutation:
    def __init__(
            self, 
            mutation_factor=0.1, 
            mutation_factor_change=None,
            mutate_elite=True
            ):
        self.mutation_factor = mutation_factor
        self.mutation_factor_change = mutation_factor_change
        self.mutate_elite = mutate_elite

    def mutate(self, gnome: np.ndarray) -> np.ndarray:
        raise NotImplementedError()
    
    def update(self):
        if self.mutation_factor_change != None:
            self.mutation_factor += self.mutation_factor_change


class MutationGenePerCity(Mutation):
    def __init__(
            self,
            mutation_factor: float = 0.1,
            mutation_factor_change = None,
            mutate_elite=True
        ):
        super().__init__(mutation_factor, mutation_factor_change, mutate_elite)

    def mutate(self, gnome: np.ndarray) -> np.ndarray:
        gnome = gnome.copy()
        for i in range(1, len(gnome)):
            if np.random.rand() < self.mutation_factor:
                while True:
                    j = np.random.randint(1, len(gnome)-1)
                    if i != j:
                        gnome[i], gnome[j] = gnome[j], gnome[i]
                        break

        return gnome


class MutationGeneDisplacement(Mutation):
    def __init__(
            self,
            mutation_factor: float = 0.1,
            mutation_factor_change = None,
            mutate_elite=True
        ):
        super().__init__(mutation_factor, mutation_factor_change, mutate_elite)

    def mutate(self, gnome: np.ndarray) -> np.ndarray:
        gnome = gnome.copy()
        if np.random.rand() < self.mutation_factor:
            n = len(gnome)
            start = np.random.randint(1, n-2)
            end = np.random.randint(start+1, n-1)
            subset = gnome[start:end+1]
            remaining = np.concatenate((gnome[:start], gnome[end+1:]))
            insert_pos = np.random.randint(1, len(remaining))
            gnome = np.concatenate((remaining[:insert_pos], subset, remaining[insert_pos:]))

        return gnome

class MutationRandomMutation(Mutation):
    def __init__(
            self,
            mutation_factor: float = 0.1,
            mutation_factor_change = None,
            mutate_elite=True,
            mutations = [MutationGenePerCity, MutationGeneDisplacement],
        ):
        super().__init__(mutation_factor, mutation_factor_change, mutate_elite)
        self.mutations = mutations

    def mutate(self, gnome: np.ndarray) -> np.ndarray:
        mutation = np.random.choice(self.mutations)
        mutation = mutation(self.mutation_factor, self.mutation_factor_change)
        return mutation.mutate(gnome)