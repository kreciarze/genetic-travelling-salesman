
from genetic_experiment_conductor import run_genetic_experiment
from travel_graph import TravelGraph
from ga_utils.crossover_functions import crossover_genes_pmx
from ga_utils.distance_functions import distance_euclidean
from ga_utils.diversification_functions import diversification_random
from ga_utils.mutation_functions import mutate_gene_per_city
from ga_utils.selection_functions import selection_elitism

available_problems = ["easy", "bays29", "berlin52", "eil101", "xqf131"]

def run_all_problems():
    for problem_name in available_problems:
        print("-" * 80)
        print(f"Running experiment for {problem_name}")
        run_genetic_experiment(             # Default values
            problem_name,                   
            travel_graph_class=TravelGraph,        
            distance_function=distance_euclidean,
            selection_function=selection_elitism,
            diversification_function=diversification_random,
            crossover_genes_function=crossover_genes_pmx,
            mutate_gene_function=mutate_gene_per_city,
            population_size=1000,           # 1000
            generations=1000,               # 500
            elitism_factor=0.15,            # 0.15
            elite_factor_change=None,       # None
            diversity_factor=0.15,          # 0.15
            diversity_factor_change=None,   # None
            crossover_factor=0.1,           # 0.1
            crossover_factor_change=None,   # None
            p_mutation=0.01,                # 0.01
            p_mutation_change=None,         # None
            mutate_elite=True,              # True
            patience=50,                    # 50
            patience_factor=0.001,          # 0.001
            verbose=2,                      # 2
        )

def main():
    
    print("Available problems:")
    for problem in available_problems:
        print(f"  - {problem}")

    problem_name = input("Enter the problem name [bays29] or 'all' to run all problems: ")
    problem_name = problem_name or "bays29"
    if problem_name == "all":
        run_all_problems()
        return

    if problem_name not in available_problems:
        print("Invalid problem name.")
        return
    
    run_genetic_experiment(             # Default values
        problem_name,                   
        travel_graph_class=TravelGraph,   
        distance_function=distance_euclidean,               
        selection_function=selection_elitism, # or selection_roulette_wheel
        diversification_function=diversification_random, # or diversification_roulette_wheel
        crossover_genes_function=crossover_genes_pmx, # or crossover_genes_edge_recombination
        mutate_gene_function=mutate_gene_per_city, # mutate_gene_displacement
        population_size=500,            # 1000
        generations=1000,               # 500
        elitism_factor=0.15,            # 0.15
        elitism_factor_change=None,     # None
        diversity_factor=0.15,          # 0.15
        diversity_factor_change=None,   # None
        crossover_factor=0.1,           # 0.1
        crossover_factor_change=None,   # None
        p_mutation=0.01,                # 0.01
        p_mutation_change=None,         # None
        mutate_elite=True,              # True
        patience=50,                    # 50
        patience_factor=0.001,          # 0.001
        verbose=2,                      # 2
    )

if __name__ == "__main__":
    main()
