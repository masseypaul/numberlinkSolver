import json

from create_grid import create_hexagonal_grid, create_rectangular_grid
from plot_functions import plot_hex, plot_rectangular

# SAT solution
with open("answer.txt", "r") as f:
    sol = f.read()
sol = sol.split(" ")

config = json.load(open("config.json"))
SIZE = config["grid_size"]
shape = config["shape"]

# Square case
# x_human = [
#     ((0, 3), (6, 4)),
#     ((1, 1), (2, 3)),
#     ((1, 4), (6, 0)),
#     ((1, 5), (3, 3)),
#     ((2, 4), (5, 2)),
# ]
# Hexagonal case
# x_human = [
#     ((0,3),(6,0)),
#     ((0,4),(6,1)),
#     ((0,5),(6,2)),
#     ((0,6),(6,3)),
#     ((1,6),(5,4)),
#     ((2,6),(3,6))
# ]
# x_human = [
#     ((0, 4), (6, 0)),
#     ((0, 6), (6, 1)),
#     ((1, 3), (3, 2)),
#     ((1, 5), (5, 3)),
#     ((2, 2), (5, 1)),
#     ((2, 5), (4, 3)),
#     ((3, 6), (6, 2)),
# ]

x_human = config["extremities"]
if x_human == []:
    raise ValueError("No extremities found in config.json. Please run the solver first.")
if shape == "rectangle":
    V, E, X = create_rectangular_grid(SIZE, x_human)
else:
    V, E, X = create_hexagonal_grid(SIZE, x_human)
    V_matrix = V.reshape(SIZE, SIZE)

# Problem parameters
N = SIZE * SIZE  # Number of vertices
K = len(X)  # Number of paths

# Create correspondence dictionaries
correspondance_dict = {}
k = 0
for v in range(N):
    for i in range(K):
        for p in range(N):
            correspondance_dict[f"x_{v}_{i}_{p}"] = k + 1
            k += 1
for i in range(K):
    for p in range(N):
        correspondance_dict[f"xphant_{i}_{p}"] = k + 1
        k += 1

correspondance_dict_inv = {v: k for k, v in correspondance_dict.items()}

# Extract the true variables from the solution
sol_strings = []
for var in sol:
    if var[0] != "-" and var != "0":  # Positive variables
        sol_strings.append(correspondance_dict_inv[int(var)])

# Parse the solution to extract the paths
paths = [[] for _ in range(K)]
for var in sol_strings:
    if var.startswith("x_"):
        _, v, i, p = var.split("_")
        paths[int(i)].append((int(p), int(v)))  # Position and vertex

# Sort each path by position
for i in range(K):
    paths[i] = [v for _, v in sorted(paths[i])]

if shape == "rectangle":
    plot_rectangular(paths, SIZE)
else:
    plot_hex(V_matrix, paths, SIZE)
