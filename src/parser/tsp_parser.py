from dataclasses import dataclass
from parser.parser import parse_headers
from typing import TextIO

import numpy as np

type Node = tuple[int, int]


@dataclass(frozen=True)
class TSPFile:
    name: str
    dimension: int
    edge_weight_type: str
    nodes: np.ndarray


def parse_tsp_file(file_path: str) -> TSPFile:
    with open(file_path, "r") as file:
        headers = parse_headers(file=file)
        nodes_list = parse_nodes(file=file)

    name = headers.get("NAME", "unknown")
    dimension = int(headers.get("DIMENSION", 0))
    edge_weight_type = headers.get("EDGE_WEIGHT_TYPE", "unknown")
    nodes = np.array(nodes_list)

    return TSPFile(
        name=name,
        dimension=dimension,
        edge_weight_type=edge_weight_type,
        nodes=nodes,
    )


def parse_nodes(file: TextIO) -> list[Node]:
    nodes = []
    edge_weight_mode = False
    for line in file:
        line = line.strip()
        if edge_weight_mode:
            if "_SECTION" in line:
                edge_weight_mode = not edge_weight_mode
            continue
        if line == "EOF":
            break
        parts = line.split()
        if len(parts) != 3:
            edge_weight_mode = True
            continue
        x, y = float(parts[1]), float(parts[2])
        nodes.append((x, y))

    return nodes
