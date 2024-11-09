import sys
from modules.constants import GRID_SIZE
from modules.ui import GridUI

def print_usage():
    print("\nUsage: python main.py <grid_type>")
    print("<grid_type>: 'default', 'warehouse'\n")

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
    if grid_type not in ['default', 'warehouse']:
        print("\nInvalid grid_type. Use -h for help.\n")
        sys.exit(1)

    start = (0, 0)
    goals = [
            (2, 2),
            (2, 9),
            (2, 17),
            (7, 3), 
            (6, 8), 
            (6, 16), 
            (13, 3), 
            (13, 8), 
            (13, 17), 
            (17, 5), 
            (17, 16),
            ]
    goal = [(19, 19)]
    ui = GridUI(grid_type, start, goals)
    ui.root.mainloop()