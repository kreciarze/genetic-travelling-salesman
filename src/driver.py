from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file

from plotter import plot_nodes_to_file
from travel_graph import TravelGraph


def main() -> None:
    tsp_file_path = "data/xqf131/xqf131.tsp"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path="data/xqf131/xqf131.png",
        title="xqf131",
    )

    tour_file_path = "data/xqf131/xqf131.tour"
    tour_file = parse_tour_file(file_path=tour_file_path)
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path="data/xqf131/xqf131_tour.png",
        title="xqf131 Tour",
        order=tour_file.tour,
    )

    travel_graph = TravelGraph(nodes=tsp_file.nodes)
    solution, distance = travel_graph.find_shortest_path()
    print(f"TSP: {tsp_file.name}")
    print(f"cities: {tsp_file.dimension}")
    print(f"edge weight type: {tsp_file.edge_weight_type}")
    print(f"best distance = {distance}")
    print(f"best solution: {solution}")
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path="data/xqf131/xqf131_solution.png",
        title="xqf131 Tour",
        order=solution,
    )


if __name__ == "__main__":
    main()
