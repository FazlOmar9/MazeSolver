import tkinter as tk
import time
from modules.algorithm import a_star
from modules.constants import *


class GridUI:
    """Class to create a grid-based UI for the A* pathfinding visualization."""

    def __init__(self, grid: str, start: tuple, goal: tuple):
        self.root = tk.Tk()
        self.grid_option = grid
        self.grid = DEFAULT_GRID if (grid == "default") else EMPTY_GRID
        self.start = start
        self.goal = goal

        self.root.title("A* Pathfinding Visualization")

        self.heading = tk.Label(
            self.root, text="Maze Optimal Path Finder using A star", font=("Helvetica", 18, "bold"))
        self.heading.pack(pady=10)

        self.canvas = tk.Canvas(
            self.root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()

        self.status_label = tk.Label(
            self.root, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        self.run_button = tk.Button(self.root, text="Run", command=lambda: self.run(
            self.start, self.goal), bg="green", fg="white", font=("Helvetica", 12, "bold"))
        self.run_button.pack(pady=10)

        self.clear_button = tk.Button(
            self.root, text="Clear", command=self.clear_grid, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.clear_button.pack(pady=10)

        self.draw_grid()

    def draw_grid(self):
        """Draw the grid based on the 2D array."""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                color = WALKABLE_COLOR if self.grid[x][y] == 1 else OBSTACLE_COLOR
                rect_id = self.canvas.create_rectangle(
                    y * CELL_SIZE, x * CELL_SIZE,
                    (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                    fill=color, outline="gray"
                )
                # toggle between 0 and 1
                self.canvas.tag_bind(
                    rect_id, "<Button-1>", lambda event, x=x, y=y: self.toggle_walkability(x, y))

    def toggle_walkability(self, x, y):
        """Toggle between walkable (1) and non-walkable (0) for a cell."""
        self.grid[x][y] = 1 - self.grid[x][y]
        new_color = WALKABLE_COLOR if self.grid[x][y] == 1 else OBSTACLE_COLOR
        self.update_cell(x, y, new_color, 0)

    def update_cell(self, x, y, color, sleep=0.0085):
        """Update the color of a specific cell."""
        self.canvas.create_rectangle(
            y * CELL_SIZE, x * CELL_SIZE,
            (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
            fill=color, outline="gray"
        )
        self.root.update()
        if sleep:
            time.sleep(sleep)

    def visualize_path(self, path, visited_nodes):
        """Visualize the A* pathfinding process."""
        self.status_label.config(text="Searching for path...")

        # Show all visited nodes
        for node in visited_nodes:
            x, y = node
            if (x, y) not in (self.start, self.goal):
                self.update_cell(x, y, VISITED_COLOR)
        time.sleep(0.5)

        self.reset_grid_colors()

        if path == None:
            self.status_label.config(text="Path not found.")
            self.update_cell(self.start[0], self.start[1], "red", 0)
            self.update_cell(self.goal[0], self.goal[1], "red", 0)
            return

        self.status_label.config(text="Tracing path...")

        for x, y in path:
            if (x, y) == self.start:
                self.update_cell(x, y, START_COLOR)
            elif (x, y) == self.goal:
                self.update_cell(x, y, GOAL_COLOR)
            else:
                self.update_cell(x, y, PATH_COLOR)

        if path:
            self.status_label.config(text="Path found. Cost: " + str(len(path) - 1))

    def reset_grid_colors(self):
        """Reset grid colors to black and white for final path tracing."""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                color = WALKABLE_COLOR if self.grid[x][y] == 1 else OBSTACLE_COLOR
                self.update_cell(x, y, color, 0)

    def clear_grid(self):
        """Reset the grid to its initial state."""
        self.grid = DEFAULT_GRID if self.grid_option == "default" else EMPTY_GRID

        self.draw_grid()
        self.status_label.config(text="Grid cleared.")

    def run(self, start, goal):
        """Run the A* algorithm and visualize the pathfinding."""
        path, visited_nodes = a_star(
            start, goal, self.grid, GRID_SIZE)
        if visited_nodes:
            self.visualize_path(path, visited_nodes)
        else:
            self.status_label.config(text="Path not found.")
