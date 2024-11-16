
from dataclasses import dataclass
from parser.parser import parse_headers
from typing import TextIO
import os

import numpy as np


@dataclass(frozen=True)
class WeightsFile:
    nodes: np.ndarray
    weights_distance_function: np.vectorize


def parse_weights_file(file_path: str, nodes) -> WeightsFile:
    if os.path.exists(file_path):
        print("Using weights file")
        weights = np.loadtxt(file_path)
        new_nodes = [i for i in range(len(nodes))]

        weights_distance_function = np.vectorize(
            lambda node_1, node_2: weights[node_1, node_2])

        return WeightsFile(
            nodes=new_nodes,
            weights_distance_function=weights_distance_function,
        )
    else:
        print("Weights file not found. Using Euclidean distance function.")
        return None
