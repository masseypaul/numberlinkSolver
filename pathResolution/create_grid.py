import numpy as np


def create_rectangular_grid(grid_size, x_human):
    V = list(range(grid_size * grid_size))
    E = []
    for x in range(grid_size):
        for y in range(grid_size):
            node = x * grid_size + y
            if x + 1 < grid_size:  # Downward edge
                E.append((node, (x + 1) * grid_size + y))
            if y + 1 < grid_size:  # Rightward edge
                E.append((node, x * grid_size + (y + 1)))
    X = []
    for i in range(len(x_human)):
        X.append(
            (
                x_human[i][0][0] * grid_size + x_human[i][0][1],
                x_human[i][1][0] * grid_size + x_human[i][1][1],
            )
        )
    return V, E, X


def create_hexagonal_grid(grid_size, x_human):
    V = np.full((grid_size, grid_size), None, dtype=object)
    id_counter = 0
    for r in range(grid_size):
        row_size = grid_size - abs(grid_size // 2 - r)
        left_offset = grid_size // 2 - r
        if left_offset >= 0:
            for q in range(row_size):
                V[r, left_offset + q] = id_counter
                id_counter += 1
        else:
            for q in range(grid_size + left_offset):
                V[r, q] = id_counter
                id_counter += 1
    E = []
    # each node is connected to all his neighbours except top left and bottom right diagonals
    total_offset = 0
    for x in range(grid_size):
        offset = grid_size // 2 - x
        if offset < 0:
            offset = abs(offset + 1)
        total_offset += offset
        for y in range(grid_size):
            if V[x, y] is not None:
                node = x * grid_size + y - total_offset
                next_line_offset = grid_size // 2 - (x + 1)
                if next_line_offset < 0:
                    next_line_offset = abs(next_line_offset + 1)
                if x + 1 < grid_size and V[x + 1, y] is not None:
                    E.append(
                        (
                            node,
                            (x + 1) * grid_size + y - total_offset - next_line_offset,
                        )
                    )
                if y + 1 < grid_size and V[x, y + 1] is not None:
                    E.append((node, x * grid_size + (y + 1) - total_offset))
                if x + 1 < grid_size and y - 1 >= 0 and V[x + 1, y - 1] is not None:
                    E.append(
                        (
                            node,
                            (x + 1) * grid_size
                            + (y - 1)
                            - total_offset
                            - next_line_offset,
                        )
                    )
    X = []
    for i in range(len(x_human)):
        X.append(
            (
                V[x_human[i][0][0], x_human[i][0][1]],
                V[x_human[i][1][0], x_human[i][1][1]],
            )
        )
    V = np.concatenate(V)
    return V, E, X
