from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file

from numpy.ma.testutils import assert_array_equal

from travel_graph import TravelGraph


def test_solution() -> None:
    tsp_file_path = "data/xqf131/xqf131.tsp"
    tour_file_path = "data/xqf131/xqf131.tour"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)
    tour_file = parse_tour_file(file_path=tour_file_path)
    assert tsp_file.name == tour_file.name
    assert tsp_file.dimension == tour_file.dimension

    travel_graph = TravelGraph(nodes=tsp_file.nodes)
    solution, distance = travel_graph.find_shortest_path()

    assert distance == 564.0
    assert_array_equal(solution, tour_file.tour)
