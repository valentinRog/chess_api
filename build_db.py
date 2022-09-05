from app.models import init_tables, Puzzle

import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        exit(1)
    init_tables()
    s = open(sys.argv[1], "r") if len(sys.argv) > 1 else sys.stdin.readlines()
    Puzzle.fill_from_csv(s, buffer_size=100)
