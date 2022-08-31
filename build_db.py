from app.models import Puzzle

import sys

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: [filename]", file=sys.stderr)
        exit(1)
    s = open(sys.argv[1], "r") if len(sys.argv) > 1 else sys.stdin.readlines()
    Puzzle.init_table()
    Puzzle.fill_from_csv(s)
