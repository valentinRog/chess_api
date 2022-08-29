import csv
import chess
from hashlib import sha256
import time
from threading import Thread

from .models import db, Puzzle
from .views import app

def fill_db():
    with open(app.config["PUZZLES_CSV_FILE"], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            puzzle = Puzzle(
                id=reader.line_num,
                division=int(sha256(row["FEN"].encode(
                    "utf-8")).hexdigest(), 16) % 100,
                elo=int(row["Rating"]),
                fen=row["FEN"],
                moves=row["Moves"],
                nb_pieces=len(chess.Board(row["FEN"]).piece_map()))
            db.session.add(puzzle)
            if not reader.line_num % 10_000:
                try:
                    db.session.commit()
                except:
                    exit()

def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    Thread(target=fill_db).start()
