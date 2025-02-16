import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from matplotlib.patches import RegularPolygon

colors = ["red", "blue", "green", "yellow", "purple"]
color_index = 0


# Function to collect start-end node pairs interactively
def select_node_pairs_rec(grid_size=6):
    x_human = []
    clicks = []
    fig, ax = plt.subplots()

    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks(range(grid_size + 1))
    ax.set_yticks(range(grid_size + 1))
    ax.grid(True)
    plt.title("Click to select and color grid cells")

    grid_colors = np.full((grid_size, grid_size), "white", dtype=object)
    cell_patches = {}

    for x in range(grid_size):
        for y in range(grid_size):
            rect = plt.Rectangle((x, y), 1, 1, color="white", ec="black")
            ax.add_patch(rect)
            cell_patches[(x, y)] = rect

    def on_click(event):
        global color_index
        if event.inaxes is not None and event.button == 1:  # Left click
            x, y = int(event.xdata), int(event.ydata)
            if (x, y) in cell_patches:
                grid_colors[x, y] = colors[color_index % len(colors)]
                cell_patches[(x, y)].set_color(grid_colors[x, y])
                plt.draw()

                clicks.append((x, y))
                if len(clicks) == 2:
                    x_human.append((clicks[0], clicks[1]))
                    print(f"Pair recorded: {clicks[0]} -> {clicks[1]}")
                    clicks.clear()
                    color_index += 1

    def stop(event):
        plt.close()

    stop_ax = plt.axes([0.8, 0.01, 0.1, 0.075])  # Position for button
    stop_button = Button(stop_ax, "Stop")
    stop_button.on_clicked(stop)
    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()

    return x_human


# Function to collect start-end node pairs interactively on a hexagonal grid
def select_node_pairs_hex(grid_size=6):
    x_human = []
    clicks = []
    fig = plt.figure(figsize=(8, 8))
    hex_radius = 1
    dx = np.sqrt(3) * hex_radius
    dy = 3 / 2 * hex_radius

    grid_colors = np.full((grid_size, grid_size), "white", dtype=object)
    hex_positions = {}
    cell_patches = {}

    for r in range(grid_size):
        mask_limit = np.abs(grid_size // 2 - r)
        for q in range(grid_size):
            if (
                r < grid_size // 2
                and q < mask_limit
                or r >= grid_size // 2
                and q >= grid_size - mask_limit
            ):
                continue
            x = r * dy
            y = q * dx + r * dx / 2
            temp = y
            y = -x
            x = temp

            hex_positions[(r, q)] = (x, y)
            hexagon = RegularPolygon(
                (x, y),
                numVertices=6,
                radius=hex_radius,
                orientation=0,
                color="white",
                ec="black",
            )
            plt.gca().add_patch(hexagon)
            cell_patches[(r, q)] = hexagon

    plt.axis("equal")
    plt.axis("off")

    def on_click(event):
        global color_index
        if event.inaxes is not None and event.button == 1:
            for (r, q), (x, y) in hex_positions.items():
                if np.hypot(event.xdata - x, event.ydata - y) < hex_radius:
                    grid_colors[r, q] = colors[color_index % len(colors)]
                    cell_patches[(r, q)].set_color(grid_colors[r, q])
                    plt.draw()
                    clicks.append((r, q))

                    if len(clicks) == 2:
                        x_human.append((clicks[0], clicks[1]))
                        print(f"Pair recorded: {clicks[0]} -> {clicks[1]}")
                        clicks.clear()
                        color_index += 1

                    break

    def stop(event):
        plt.close()

    stop_ax = plt.axes([0.8, 0.01, 0.1, 0.075])
    stop_button = Button(stop_ax, "Stop")
    stop_button.on_clicked(stop)
    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()

    return x_human
