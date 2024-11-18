from typing import Any, Callable
import numpy as np

type DistanceFunction = Callable[[Any, Any], float]


def distance_euclidean(node_1: np.ndarray, node_2: np.ndarray) -> float:
    return float(np.linalg.norm(node_1 - node_2))
