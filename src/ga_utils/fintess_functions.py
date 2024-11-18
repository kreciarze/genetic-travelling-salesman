from typing import Any, Callable
import numpy as np

from ga_utils.distance_functions import DistanceFunction, distance_euclidean

type FitnessFunction = Callable[[np.ndarray, Any, DistanceFunction], float]


def fitness_classic(gnome: np.ndarray, nodes: Any, distance_function: DistanceFunction = distance_euclidean):

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
