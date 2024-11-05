import numpy as np
from numpy import array_equal

from travel_graph import euclidean_distance, TravelGraph


def test_euclidean_distance() -> None:
    node_1 = np.array([0, 0])
    node_2 = np.array([3, 4])
    expected = 5.0
    assert euclidean_distance(node_1, node_2) == expected


def test_solution() -> None:
    nodes = np.array(
        [
            [0, 0],
            [3, 4],
            [6, 8],
            [9, 12],
            [12, 16],
            [12, 0],
        ]
    )
    travel_graph = TravelGraph(nodes=nodes)
    solution, distance = travel_graph.find_shortest_path()

    assert distance == 48.0
    start_idx = np.where(solution == 0)[0][0]
    solution = np.roll(solution, -start_idx)

    alt1 = array_equal(solution, [0, 1, 2, 3, 4, 5])
    alt2 = array_equal(solution, [0, 5, 4, 3, 2, 1])
    assert alt1 or alt2
