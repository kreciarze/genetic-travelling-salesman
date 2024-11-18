
from genetic_experiment_conductor import run_genetic_experiment
from travel_graph_classic import TravelGraphClassic

available_problems = ["easy", "bays29", "berlin52", "eil101", "xqf131"]

def run_all_problems():
    for problem_name in available_problems:
        print("-" * 80)
        print(f"Running experiment for {problem_name}")
        run_genetic_experiment(             # Default values
            problem_name,                   
            travel_graph_class=TravelGraphClassic,
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
        travel_graph_class=TravelGraphClassic,
        population_size=500,           # 1000
        generations=1000,               # 500
        elitism_factor=0.15,             # 0.15
        elitism_factor_change=None,       # None
        diversity_factor=0.15,           # 0.15
        diversity_factor_change=None,   # None
        crossover_factor=0.03,           # 0.1
        crossover_factor_change=None, # None
        p_mutation=0.01,                # 0.01
        p_mutation_change=None,         # None
        mutate_elite=True,              # True
        patience=50,                    # 50
        patience_factor=0.001,          # 0.001
        verbose=2,                      # 2
    )

if __name__ == "__main__":
    main()
