# Python3 implementation of the above approach
from random import randint

from typing import Any, Callable
import numpy as np

import time
from parser.tour_parser import parse_tour_file
from parser.tsp_parser import parse_tsp_file

from plotter import plot_nodes_to_file
from travel_graph import TravelGraph


type DistanceFunction = Callable[[Any, Any], float]


def euclidean_distance(node_1: np.ndarray, node_2: np.ndarray) -> float:
    return float(np.linalg.norm(node_1 - node_2))


class Individual:
    def __init__(self) -> None:
        self.gnome: np.array = np.array([])
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return f"Individual(gnome: {self.gnome}, fitness: {round(self.fitness,2)})"


class TravelGraphClassic:

    def __init__(
        self,
        nodes: np.ndarray,
        distance_function: DistanceFunction = euclidean_distance,
    ) -> None:
        self.nodes = nodes
        self.distance_function = distance_function
        self.V = len(nodes)
        self.all_time_best = float("inf")

    @staticmethod
    def rand_num(start, end):
        return randint(start, end-1)

    def create_gnome(self):
        gnome = [0]
        while True:
            if len(gnome) == self.V:
                gnome.append(gnome[0])
                break

            v = TravelGraphClassic.rand_num(0, self.V)
            if not v in gnome:
                gnome.append(v)

        return np.array(gnome)

    def mutate_gene(self, gnome):
        gnome = gnome.copy()
        while True:
            r = TravelGraphClassic.rand_num(1, self.V)
            r1 = TravelGraphClassic.rand_num(1, self.V)
            if r1 != r:
                temp = gnome[r]
                gnome[r] = gnome[r1]
                gnome[r1] = temp
                break
        return gnome

    def fitness_function(gnome):

        f = 0
        for i in range(len(gnome) - 1):
            a = gnome[i]
            b = gnome[i + 1]

            node_a = nodes[a]
            node_b = nodes[b]

            f += euclidean_distance(node_a, node_b)

        e = gnome[len(gnome) - 1]
        s = gnome[0]
        node_end = nodes[e]
        node_start = nodes[s]

        f += euclidean_distance(node_end, node_start)

        return f

    @staticmethod
    def cooldown(temp):
        return (90 * temp) / 100

    def find_shortest_path(
        self,
        population_size=10,
        generations=10,
        temperature=10000,
        elitism_factor=0.2
    ):
        i_generation = 1

        population = []

        for i in range(population_size):
            temp = Individual()
            temp.gnome = self.create_gnome()
            temp.fitness = TravelGraphClassic.fitness_function(temp.gnome)
            population.append(temp)

        print("\nInitial population:")
        for i in range(population_size):
            print("\t", population[i])
        print()

        while temperature > 1000 and i_generation <= generations:
            population.sort()
            print("\nCurrent temp: ", temperature)
            new_population = []

            for i in range(population_size):
                p1 = population[i]

                while True:
                    new_gnome = Individual()
                    new_gnome.gnome = self.mutate_gene(p1.gnome)
                    new_gnome.fitness = TravelGraphClassic.fitness_function(
                        new_gnome.gnome)

                    if new_gnome.fitness <= population[i].fitness:
                        new_population.append(new_gnome)
                        break

                    else:

                        # Accepting the rejected children at
                        # a possible probability above threshold.
                        prob = pow(
                            2.7,
                            -1
                            * (
                                (float)(new_gnome.fitness -
                                        population[i].fitness)
                                / temperature
                            ),
                        )
                        if prob > 0.5:
                            new_population.append(new_gnome)
                            break

            temperature = TravelGraphClassic.cooldown(temperature)
            population = new_population
            print("Generation", i_generation)

            # for i in range(population_size):
            #     print(population[i])

            sorted_population = sorted(population, key=lambda x: x.fitness)
            print(sorted_population[0], end=" ")
            print("- population best")
            self.all_time_best = min(
                self.all_time_best, sorted_population[0].fitness)

            i_generation += 1

        print("\n\nAll-time best solution: ", self.all_time_best)


if __name__ == "__main__":

    # problem_name = input("Enter the problem name [xqf131]: ")
    # problem_name = problem_name or "xqf131"
    problem_name = "xqf131"
    # problem_name = "easy"
    tsp_file_path = f"data/{problem_name}/{problem_name}.tsp"
    tsp_file = parse_tsp_file(file_path=tsp_file_path)
    nodes = tsp_file.nodes
    # plot_nodes_to_file(
    #     nodes=nodes,
    #     file_path=f"data/{problem_name}/{problem_name}.png",
    #     title="easy",
    # )

    tour_file_path = f"data/{problem_name}/{problem_name}.tour"
    tour_file = parse_tour_file(file_path=tour_file_path)
    # plot_nodes_to_file(
    #     nodes=tsp_file.nodes,
    #     file_path=f"data/{problem_name}/{problem_name}_tour.png",
    #     title=f"{problem_name} Tour",
    #     order=tour_file.tour,
    # )

    # travel_graph = TravelGraph(nodes=nodes)
    # print(nodes)

    p_test = [0, 1, 2, 3, 4, 5]
    f_val = TravelGraphClassic.fitness_function(p_test)
    # print(f_val)

    # start_time = time.perf_counter()
    travel_graph = TravelGraphClassic(
        nodes=nodes,
    )
    travel_graph.find_shortest_path(
        population_size=100,
        generations=100,
        temperature=10000
    )
    # end_time = time.perf_counter()

    # p_a = [0, 1, 2, 3, 4, 5]
    # p_b = [0, 2, 1, 5, 4, 3]
    # g_crossed = travel_graph.crossover_genes(p_a, p_b)
    # print(g_crossed)
