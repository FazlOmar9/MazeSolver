def heuristic(a: tuple, b: tuple) -> int:
    """Calculate Manhattan distance between two points"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(node: tuple, grid: list, n: int) -> list:
    """Get walkable neighbors"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, down, left, right
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
            neighbors.append((nx, ny))
    return neighbors


def reconstruct_path(came_from: dict, start: tuple, goal: tuple) -> list:
    """Reconstruct the path from start to goal using came_from dict"""
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return path[::-1]  # Return path from start to goal
