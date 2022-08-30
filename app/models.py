import csv
import chess
from hashlib import sha256

from flask_sqlalchemy import SQLAlchemy

from .views import app


db = SQLAlchemy(app)


class Puzzle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    division = db.Column(db.Integer(), index=True,
                         unique=False, nullable=False)
    elo = db.Column(db.Integer(), unique=False, nullable=False)
    fen = db.Column(db.String(200), unique=False, nullable=False)
    moves = db.Column(db.String(500), unique=False, nullable=False)
    nb_pieces = db.Column(db.Integer(), unique=False, nullable=False)

    def __iter__(self):
        for key, value in {
            "id": self.id,
            "elo": self.elo,
            "fen": self.fen,
            "moves": self.moves.split(),
            "nb_pieces": self.nb_pieces,
            "pieces": chess.Board(self.fen).piece_map()
            }.items():
            yield (key, value)

    def build():
        Puzzle.__table__.drop(db.engine)
        db.create_all()
        db.session.commit()
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
                db.session.commit()
