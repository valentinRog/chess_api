import csv
import chess
from flask_sqlalchemy import SQLAlchemy

from .views import app

db = SQLAlchemy(app)


class Puzzle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    elo = db.Column(db.Integer(), unique=False, nullable=False)
    fen = db.Column(db.String(200), unique=False, nullable=False)
    moves = db.Column(db.String(500), unique=False, nullable=False)
    nb_pieces = db.Column(db.Integer(), unique=False, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "elo": self.elo,
            "fen": self.fen,
            "moves": self.nb_pieces,
            "nb_pieces": self.nb_pieces}


def init_db():
    db.drop_all()
    db.create_all()
    with open(app.config["PUZZLES_CSV_FILE"], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            puzzle = Puzzle(
                id=reader.line_num,
                elo=int(row["Rating"]),
                fen=row["FEN"],
                moves=row["Moves"],
                nb_pieces=len(chess.Board(row["FEN"]).piece_map()))
            db.session.add(puzzle)
            if not reader.line_num % 10000:
                db.session.commit()
        db.session.commit()
