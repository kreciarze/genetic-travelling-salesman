from typing import Any, Callable
import numpy as np

type MutationFunction = Callable[[np.ndarray, float], np.ndarray]


def mutate_gene_per_city(gnome, p_mutation=0.007):
    gnome = gnome.copy()
    for i in range(1, len(gnome)):
        if np.random.rand() < p_mutation:
            while True:
                j = np.random.randint(1, len(gnome)-1)
                if i != j:
                    gnome[i], gnome[j] = gnome[j], gnome[i]
                    break

    return gnome


def mutate_gene_displacement(gnome, p_mutation=0.07):

    if np.random.rand() > p_mutation:
        return gnome

    # Step 1: Select a subset
    n = len(gnome)
    # Ensure at least two elements remain for mutation
    start = np.random.randint(1, n - 2)
    end = np.random.randint(start + 1, n - 1)
    subset = gnome[start:end + 1]

    # Step 2: Remove the subset
    remaining = np.concatenate((gnome[:start], gnome[end + 1:]))

    # Step 3: Reinsert the subset
    # Position in the remaining list
    insert_pos = np.random.randint(1, len(remaining))
    mutated_solution = np.concatenate(
        (remaining[:insert_pos], subset, remaining[insert_pos:]))

    return mutated_solution
