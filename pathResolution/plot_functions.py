import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import RegularPolygon


# Convert vertex indices to grid coordinates
def index_to_grid(v, grid_size):
    return divmod(v, grid_size)  # Returns (row, col)


def index_to_grid_hex(v, grid_size, V_matrix):
    count = 0
    for y in range(grid_size):
        for x in range(grid_size):
            if V_matrix[y][x] is not None:
                if count == v:
                    return (y, x)
                count += 1
    return None


def plot_hex(V_matrix, paths, grid_size):
    paths_grid = []
    for path in paths:
        paths_grid.append(
            [index_to_grid_hex(v, grid_size, V_matrix) for v in path]
        )  # Convert to grid coordinates
    plt.figure(figsize=(8, 8))

    # Hexagonal grid setup
    hex_radius = 1
    dx = np.sqrt(3) * hex_radius
    dy = 3 / 2 * hex_radius

    # Positions of hexagons
    hex_positions = {}
    for r in range(grid_size):
        for q in range(grid_size):
            if V_matrix[r][q] is not None:
                x = r * dy
                y = q * dx + r * dx / 2
                temp = y
                y = -x
                x = temp
                hex_positions[(r, q)] = (x, y)

    # Plot the hexagonal grid
    for (r, q), (x, y) in hex_positions.items():
        hexagon = RegularPolygon(
            (x, y),
            numVertices=6,
            radius=hex_radius,
            orientation=0,
            color="lightgray",
            ec="black",
        )
        plt.gca().add_patch(hexagon)

    # # Add the paths to the plot
    colors = ["red", "blue", "green", "orange", "purple", "pink"]
    for i, path in enumerate(paths_grid):
        path_coords = [hex_positions[coord] for coord in path]
        path_edges = [
            (path_coords[j], path_coords[j + 1]) for j in range(len(path_coords) - 1)
        ]

        # Plot edges
        for (x1, y1), (x2, y2) in path_edges:
            plt.plot([x1, x2], [y1, y2], color=colors[i % len(colors)], lw=2, alpha=0.5)

        # Plot nodes
        for x, y in path_coords:
            plt.plot(
                x, y, marker="o", color=colors[i % len(colors)], markersize=8, alpha=0.7
            )

    plt.title("Numberlink Solution")
    plt.axis("equal")
    plt.show()


def plot_rectangular(paths, grid_size):
    paths_grid = []
    for path in paths:
        paths_grid.append(
            [index_to_grid(v, grid_size) for v in path]
        )  # Convert to grid coordinates

    # Plot the solution
    G = nx.grid_2d_graph(grid_size, grid_size)
    pos = {(x, y): (y, -x) for x, y in G.nodes()}  # Position nodes in grid layout

    plt.figure(figsize=(8, 8))
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_color="lightgray",
        node_size=500,
        edge_color="gray",
    )

    # Add the paths to the plot
    colors = ["red", "blue", "green", "orange", "purple"]
    for i, path in enumerate(paths_grid):
        path_edges = [(path[j], path[j + 1]) for j in range(len(path) - 1)]
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=path_edges,
            edge_color=colors[i % len(colors)],
            width=2.5,
            alpha=0.5,
        )
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=path,
            node_color=colors[i % len(colors)],
            node_size=600,
            alpha=0.5,
        )

    plt.title("Numberlink Solution")
    plt.show()
