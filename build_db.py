from app import app
from app import models

import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(1)
    with app.app_context():
        while True:
            try:
                models.init_tables()
            except:
                time.sleep(2)
            else:
                break
        models.Puzzle.fill_from_csv(sys.argv[1], buffer_size=100)
