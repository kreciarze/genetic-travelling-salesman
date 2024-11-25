
from genetic_experiment_conductor import run_genetic_experiment
from travel_graph import TravelGraph
from ga_utils.crossover_functions import CrossoverGenesPMX
from ga_utils.distance_functions import distance_euclidean
from ga_utils.diversification_functions import diversification_random
from ga_utils.mutation_functions import MutationRandomMutation
from ga_utils.selection_functions import SelectionTournament

available_problems = ["easy", "bays29", "berlin52", "eil101", "xqf131"]

def main():
    
    print("Available problems:")
    for problem in available_problems:
        print(f"  - {problem}")

    problem_name = input("Enter the problem name [bays29]: ")
    problem_name = problem_name or "bays29"

    if problem_name not in available_problems:
        print("Invalid problem name.")
        return
    
    population_size = 1000
    generations = 1000
    
    selection = SelectionTournament(
        selection_factor=0.15,
        tournament_factor=0.4,
        selection_p=0.8
    )
    
    crossover = CrossoverGenesPMX(
        crossover_factor=0.1,
        # crossover_factor_change=-0.05/40,
        # use_factor_as_range=True
    )

    mutation = MutationRandomMutation(
        mutation_factor=0.01,
        # mutation_factor_change=0.1/50,
        mutate_elite=True,
    )
    
    run_genetic_experiment(
        problem_name,                   
        travel_graph_class=TravelGraph,   
        distance_function=distance_euclidean,               
        selection=selection,
        diversification_function=diversification_random, # or diversification_roulette_wheel
        crossover=crossover,
        mutation=mutation,
        population_size=population_size,
        generations=generations,
        diversity_factor=.2,          # 0.15
        diversity_factor_change=None,   # None
        patience=50,                    # 50
        patience_factor=0.001,          # 0.001
        verbose=2,                      # 2
    )

if __name__ == "__main__":
    main()
