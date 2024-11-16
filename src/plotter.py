import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray


def plot_nodes_to_file(
    nodes: np.ndarray,
    file_path: str,
    title: str = "TSP Path",
    order: ndarray | None = None,
) -> None:
    x_coords = nodes[:, 0]
    y_coords = nodes[:, 1]

    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()

    padding = 10 * (x_max - x_min) / 800
    x_min, x_max = x_min - padding, x_max + padding
    y_min, y_max = y_min - padding, y_max + padding

    width = x_max - x_min
    height = y_max - y_min
    aspect_ratio = width / height

    plt.figure(figsize=(8 * aspect_ratio, 8))
    plt.scatter(x_coords, y_coords, s=6)

    if order is not None:
        plt.plot(np.append(x_coords[order], x_coords[order][0]), np.append(
            y_coords[order], y_coords[order][0]), linewidth=1)

    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.gca().invert_yaxis()
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.tight_layout(pad=1)
    plt.savefig(file_path, format="png", dpi=100)
    plt.close()


def plot_convergence_to_file(
    convergence: np.ndarray,
    file_path: str,
    title: str = "Convergence",
) -> None:
    plt.figure(figsize=(8, 8))
    plt.plot(convergence)
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid()
    plt.tight_layout(pad=1)
    plt.savefig(file_path, format="png", dpi=100)
    plt.close()
