from numpy.ma.testutils import assert_array_equal

from travel_graph import TravelGraph


def test_solution() -> None:
    cities = ["City 1", "City 2", "City 3"]
    distance_matrix = [
        [0.0, 1.0, 9.0],
        [9.0, 0.0, 1.0],
        [1.0, 9.0, 0.0],
    ]
    travel_graph = TravelGraph(city_names=cities, distance_matrix=distance_matrix)
    solution, distance = travel_graph.find_shortest_path()

    assert distance == 3.0
    assert_array_equal(solution, ["City 1", "City 2", "City 3"])
