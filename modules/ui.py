import tkinter as tk
import time
from modules.algorithm import a_star
from modules.constants import *


class GridUI:
    """Class to create a grid-based UI for the A* pathfinding visualization."""

    def __init__(self, grid: str, start: tuple, goals: list):
        self.root = tk.Tk()
        self.grid_option = grid
        self.grid = DEFAULT_GRID if grid == "default" else AMAZON_WAREHOUSE_GRID
        self.start = start
        self.goals = goals

        self.root.title("A* Pathfinding Visualization")

        self.heading = tk.Label(
            self.root, text="Warehouse Path Finder for N Jobs", font=("Helvetica", 18, "bold"))
        self.heading.pack(pady=10)

        self.canvas = tk.Canvas(
            self.root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()

        self.status_label = tk.Label(
            self.root, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        self.job_label = tk.Label(
            self.root, text="Jobs completed: 0", font=("Helvetica", 14))
        self.job_label.pack(pady=10)

        self.run_button = tk.Button(self.root, text="Run", command=lambda: self.run(
            self.start, self.goals), bg="green", fg="white", font=("Helvetica", 12, "bold"))
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

    def update_cell(self, x, y, color, sleep=0.001):
        """Update the color of a specific cell."""
        self.canvas.create_rectangle(
            y * CELL_SIZE, x * CELL_SIZE,
            (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
            fill=color, outline="gray"
        )
        self.root.update()
        if sleep:
            time.sleep(sleep)

    def visualize_path(self, path, visited_nodes, start, goal):
        """Visualize the A* pathfinding process."""
        self.status_label.config(text="Searching for path...")

        # Show all visited nodes
        for node in visited_nodes:
            x, y = node
            if (x, y) not in (start, goal):
                self.update_cell(x, y, VISITED_COLOR)
        time.sleep(0.5)

        self.reset_grid_colors()

        if path == None:
            self.status_label.config(text="Path not found.")
            self.update_cell(start[0], start[1], "red", 0)
            self.update_cell(goal[0], goal[1], "red", 0)
            return

        self.status_label.config(text="Tracing path...")

        for x, y in path:
            if (x, y) == start:
                self.update_cell(x, y, START_COLOR)
            elif (x, y) == goal:
                self.update_cell(x, y, GOAL_COLOR)
            else:
                self.update_cell(x, y, PATH_COLOR, 0.005)

        if path:
            self.status_label.config(text="Path found. Cost: " + str(len(path) - 1))
        time.sleep(1)

    def reset_grid_colors(self):
        """Reset grid colors to black and white for final path tracing."""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                color = WALKABLE_COLOR if self.grid[x][y] == 1 else OBSTACLE_COLOR
                self.update_cell(x, y, color, 0)

    def clear_grid(self):
        """Reset the grid to its initial state."""
        self.grid = DEFAULT_GRID if self.grid_option == "default" else AMAZON_WAREHOUSE_GRID

        self.draw_grid()
        self.status_label.config(text="Grid cleared.")

    def run(self, start, goals):
        """Run the A* algorithm sequentially for each goal in the list."""
        for i, goal in enumerate(goals):
            path, visited_nodes = a_star(start, goal, self.grid, GRID_SIZE)
            
            if path:
                self.visualize_path(path, visited_nodes, start, goal)
                start = goal  # Set the next start to the current goal

                if i < len(goals) - 1:  # Only clear if not the last goal
                    self.clear_visited_nodes(visited_nodes)
                
                self.job_label.config(text=f"Jobs completed: {i + 1}")
            else:
                self.status_label.config(text=f"Path to goal {goal} not found.")
                break  # Stop if a goal is unreachable
    
    def clear_visited_nodes(self, visited_nodes):
        """Clear visited nodes from the grid, keeping only path cells."""
        for x, y in visited_nodes:
            if self.grid[x][y] == 1:
                self.update_cell(x, y, WALKABLE_COLOR, 0)
