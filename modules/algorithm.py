import heapq
from modules.helper import heuristic, get_neighbors, reconstruct_path

def a_star(start: tuple, goal: tuple, grid: list, n: int) -> tuple:
    """Perform A* search to find the shortest path from start to goal and track visited nodes."""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited_nodes = []  # Track nodes visited during the search

    while open_set:
        current = heapq.heappop(open_set)[1]
        visited_nodes.append(current)  # Record the current node as visited

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return path, visited_nodes  # Return both the final path and visited nodes

        for neighbor in get_neighbors(current, grid, n):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, visited_nodes  # Return None for the path if no path is found, along with visited nodes
