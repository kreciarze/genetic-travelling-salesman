from parser.tsp_parser import parse_tsp_file

from travel_graph import TravelGraph


def main() -> None:
    tsp_file_path = "data/xqf131/xqf131.tsp"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)

    travel_graph = TravelGraph(nodes=tsp_file.nodes)
    solution, distance = travel_graph.find_shortest_path()
    print(f"TSP: {tsp_file.name}")
    print(f"cities: {tsp_file.dimension}")
    print(f"edge weight type: {tsp_file.edge_weight_type}")
    print()
    print(f"best solution: {" -> ".join(solution)}")
    print(f"best distance = {distance}")


if __name__ == "__main__":
    main()
