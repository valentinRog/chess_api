import csv
import chess
from hashlib import sha256
import time

from .models import db, Puzzle
from .views import app

from time import time

def fill_db():
    with open(app.config["PUZZLES_CSV_FILE"], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = time()
            puzzle = Puzzle(
                id=reader.line_num,
                division=int(sha256(row["FEN"].encode(
                    "utf-8")).hexdigest(), 16) % 100,
                elo=int(row["Rating"]),
                fen=row["FEN"],
                moves=row["Moves"],
                nb_pieces=len(chess.Board(row["FEN"]).piece_map()))
            db.session.add(puzzle)
            if not reader.line_num % 10000:
                db.session.commit()
        db.session.commit()

def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    fill_db()
