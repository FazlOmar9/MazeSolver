GRID_SIZE = 7
CELL_SIZE = 70
WALKABLE_COLOR = "white"
OBSTACLE_COLOR = "black"
START_COLOR = "red"
GOAL_COLOR = "green"
PATH_COLOR = "blue"
VISITED_COLOR = "orange"
DEFAULT_GRID = [
    [1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]
EMPTY_GRID = [[1] * GRID_SIZE for _ in range(GRID_SIZE)]
