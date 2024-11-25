import time

from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file
from parser.weights_parser import parse_weights_file

from solution_exporter import save_solution_to_file
from plotter import plot_convergence_to_file, plot_nodes_to_file

from travel_graph import TravelGraph
from ga_utils.distance_functions import distance_euclidean
from ga_utils.crossover_functions import CrossoverGenesPMX
from ga_utils.diversification_functions import diversification_random
from ga_utils.mutation_functions import MutationRandomMutation
from ga_utils.selection_functions import SelectionTournament



def run_genetic_experiment(
        problem_name, 
        travel_graph_class=TravelGraph,
        distance_function=distance_euclidean,
        selection=SelectionTournament(),
        diversification_function=diversification_random,
        crossover=CrossoverGenesPMX(),
        mutation=MutationRandomMutation(),
        **kwargs_find_shortest_path
    ):

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
    distance_function = distance_euclidean
    weights_file_path = f"data/{problem_name}/{problem_name}.weights"
    weights_file = parse_weights_file(
        file_path=weights_file_path, nodes=tsp_file.nodes)
    if weights_file is not None:
        nodes = weights_file.nodes
        distance_function = weights_file.weights_distance_function

    # solve the problem
    travel_graph = travel_graph_class(
        nodes=nodes,
        distance_function=distance_function,
        selection = selection,
        diversification_function = diversification_function,
        crossover = crossover,
        mutation = mutation,
    )
    start_time = time.perf_counter()
    try:
        travel_graph.find_shortest_path(
            **kwargs_find_shortest_path
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
