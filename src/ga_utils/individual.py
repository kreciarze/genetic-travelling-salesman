import numpy as np


class Individual:
    def __init__(
            self,
            V = None
        ) -> None:
        self.gnome: np.array = Individual.create_gnome(V) if V else np.array([])
        self.fitness = 0

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return f"Individual(gnome: {self.gnome}, fitness: {round(self.fitness, 2)})"
    

    @staticmethod
    def create_gnome(V):
        gnome = [0]
        while True:
            if len(gnome) == V:
                gnome.append(gnome[0])
                break

            v = np.random.randint(0, V)
            if not v in gnome:
                gnome.append(v)

        return np.array(gnome)
    