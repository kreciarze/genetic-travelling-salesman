from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file


def test_tsp_parser() -> None:
    file_path = "data/xqf131/xqf131.tsp"
    tsp_file = parse_tsp_file(file_path=file_path)

    assert tsp_file.name == "xqf131"
    assert tsp_file.dimension == 131
    assert tsp_file.edge_weight_type == "EUC_2D"
    assert tsp_file.nodes.shape == (131, 2)


def test_tour_parser() -> None:
    file_path = "data/xqf131/xqf131.tour"
    tour_file = parse_tour_file(file_path=file_path)

    assert tour_file.name == "xqf131"
    assert tour_file.dimension == 131
    assert len(tour_file.tour) == 131
