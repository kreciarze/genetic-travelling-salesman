import time
from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file

from plotter import plot_nodes_to_file
from travel_graph import TravelGraph


def main() -> None:
    problem_name = input("Enter the problem name [xqf131]: ")
    problem_name = problem_name or "xqf131"
    tsp_file_path = f"data/{problem_name}/{problem_name}.tsp"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)
    nodes = tsp_file.nodes
    plot_nodes_to_file(
        nodes=nodes,
        file_path=f"data/{problem_name}/{problem_name}.png",
        title="easy",
    )

    tour_file_path = f"data/{problem_name}/{problem_name}.tour"
    tour_file = parse_tour_file(file_path=tour_file_path)
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path=f"data/{problem_name}/{problem_name}_tour.png",
        title=f"{problem_name} Tour",
        order=tour_file.tour,
    )

    travel_graph = TravelGraph(nodes=nodes)

    start_time = time.perf_counter()
    solution, distance = travel_graph.find_shortest_path()
    end_time = time.perf_counter()

    print(f"TSP: {tsp_file.name}")
    print(f"cities: {tsp_file.dimension}")
    print(f"edge weight type: {tsp_file.edge_weight_type}")
    print(f"best distance = {distance}")
    print(f"best solution: {solution}")
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
    plot_nodes_to_file(
        nodes=nodes,
        file_path=f"data/{problem_name}/{problem_name}_solution.png",
        title=f"{problem_name} Tour",
        order=solution,
    )


if __name__ == "__main__":
    main()
