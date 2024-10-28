from random import random

from travel_graph import TravelGraph


def main() -> None:
    cities = [f"City {i}" for i in range(0, 100)]
    distance_matrix = generate_random_distance_matrix(cities=cities)
    print(f"Distance Matrix: {distance_matrix}")

    travel_graph = TravelGraph(city_names=cities, distance_matrix=distance_matrix)
    solution, distance = travel_graph.find_shortest_path()
    print(f"Best solution: {" -> ".join(solution)}")
    print(f"Distance of the best solution = {distance}")


def generate_random_distance_matrix(cities: list[str]) -> list[list[float]]:
    distance_matrix = []

    for city_1 in cities:
        city_1_distances = []

        for city_2 in cities:
            if city_1 == city_2:
                city_1_distances.append(0.0)
            else:
                city_1_distances.append(random())

        distance_matrix.append(city_1_distances)

    return distance_matrix


if __name__ == "__main__":
    main()
