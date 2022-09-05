from app.models import init_tables, Puzzle

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(1)
    init_tables()
    Puzzle.fill_from_csv(sys.argv[1], buffer_size=100)
