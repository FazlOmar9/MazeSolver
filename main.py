import sys
from modules.constants import GRID_SIZE
from modules.ui import GridUI

def print_usage():
    print("\nUsage: python main.py <grid_type>")
    print("<grid_type>: 'default', 'empty'\n")

def argument_usage():
    print("\nExpected 1 argument, got", len(sys.argv) - 1)
    print("Use -h for help.\n")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        argument_usage()
        sys.exit(1)

    if sys.argv[1] == "-h":
        print_usage()
        sys.exit(0)

    grid_type = sys.argv[1]
    if grid_type not in ['default', 'empty']:
        print("\nInvalid grid_type. Use -h for help.\n")
        sys.exit(1)

    start = (0, 0)
    goal = (GRID_SIZE - 1, GRID_SIZE - 1)

    ui = GridUI(grid_type, start, goal)
    ui.root.mainloop()