from pygad import GA

from travel_graph import TravelGraph


def main() -> None:
    city_names = ["City 1", "City 2", "City 3", "City 4", "City 5"]
    travel_graph = TravelGraph(city_names=city_names)

    ga_instance = GA(
        num_generations=50,
        num_parents_mating=2,
        fitness_func=travel_graph.fitness_function,
        sol_per_pop=50,
        num_genes=len(city_names),
        init_range_low=0,
        init_range_high=len(city_names) - 1,
        gene_type=int,
        parent_selection_type="sss",
        keep_parents=1,
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=10,
    )
    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))


if __name__ == "__main__":
    main()
