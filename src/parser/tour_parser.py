from dataclasses import dataclass
from parser.parser import parse_headers
from typing import TextIO

import numpy as np


@dataclass(frozen=True)
class TourFile:
    name: str
    dimension: int
    tour: np.ndarray


def parse_tour_file(file_path: str) -> TourFile:
    with open(file_path, "r") as file:
        headers = parse_headers(file=file)
        tour = parse_tour(file=file)

    name = headers.get("NAME", "unknown")
    dimension = int(headers.get("DIMENSION", 0))

    np_tour = np.array(tour) - 1
    return TourFile(name=name, dimension=dimension, tour=np_tour)


def parse_tour(file: TextIO) -> list[int]:
    tour = []
    for line in file:
        line = line.strip()
        if line == "-1":
            break
        tour.append(int(line))

    return tour
