import time

from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file
from parser.weights_parser import parse_weights_file

from solution_exporter import save_solution_to_file
from plotter import plot_convergence_to_file, plot_nodes_to_file

from travel_graph_classic import TravelGraphClassic, euclidean_distance
from travel_graph import TravelGraph


def main():

    # choose the problem
    avaliable_problems = ["easy", "bays29", "berlin52", "eil101", "xqf131"]
    print("Avaliable problems:")
    for problem in avaliable_problems:
        print(f"  - {problem}")

    problem_name = input("Enter the problem name [bays29]: ")
    problem_name = problem_name or "bays29"

    # parse the files
    # get tsp file
    tsp_file_path = f"data/{problem_name}/{problem_name}.tsp"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)
    nodes = tsp_file.nodes
    plot_nodes_to_file(
        nodes=nodes,
        file_path=f"data/{problem_name}/{problem_name}.png",
        title=f"{problem_name} Nodes",
    )

    # get tour file
    tour_file_path = f"data/{problem_name}/{problem_name}.tour"
    tour_file = parse_tour_file(file_path=tour_file_path)
    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path=f"data/{problem_name}/{problem_name}_tour.png",
        title=f"{problem_name} Tour",
        order=tour_file.tour,
    )

    # get weights file (if exists)
    distance_function = euclidean_distance
    weights_file_path = f"data/{problem_name}/{problem_name}.weights"
    weights_file = parse_weights_file(
        file_path=weights_file_path, nodes=tsp_file.nodes)
    if weights_file.weights_distance_function is not None:
        nodes = weights_file.nodes
        distance_function = weights_file.weights_distance_function

    # solve the problem
    travel_graph = TravelGraphClassic(
        nodes=nodes,
        distance_function=distance_function,
    )
    start_time = time.perf_counter()
    try:
        travel_graph.find_shortest_path(
            population_size=500,  # 500
            generations=500,  # 500
            elitism_factor=0.15,  # 0.15
            diversity_factor=0.15,  # 0.15
            linear_selection_factor=0.5,  # 0.5
            crossover_factor=10/131,  # 10/131
            p_mutation=0.01,  # 0.01
            mutate_elite=True,  # True
            patience=50,  # 50
            patience_factor=0.001,  # 0.001
            verbose=2,  # 2
        )
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by the user.")
    end_time = time.perf_counter()

    solution = travel_graph.get_solution()
    distance = travel_graph.get_fitness()
    convergence = travel_graph.get_convergence()

    save_solution_to_file(
        solution=solution,
        fitness=distance,
        file_path=f"data/{problem_name}/{problem_name}_solution.tour",
        time_elapsed=end_time-start_time,
    )

    plot_nodes_to_file(
        nodes=tsp_file.nodes,
        file_path=f"data/{problem_name}/{problem_name}_solution.png",
        title=f"{problem_name} Solution",
        order=solution,
    )

    plot_convergence_to_file(
        convergence=convergence,
        file_path=f"data/{problem_name}/{problem_name}_convergence.png",
        title=f"{problem_name} Convergence",
    )


if __name__ == "__main__":
    main()
