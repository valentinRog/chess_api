import chess
from flask_sqlalchemy import SQLAlchemy

from .views import app

db = SQLAlchemy(app)

class Puzzle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    division = db.Column(db.Integer(), index=True, unique=False, nullable=False)
    elo = db.Column(db.Integer(), unique=False, nullable=False)
    fen = db.Column(db.String(200), unique=False, nullable=False)
    moves = db.Column(db.String(500), unique=False, nullable=False)
    nb_pieces = db.Column(db.Integer(), unique=False, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "elo": self.elo,
            "fen": self.fen,
            "moves": self.moves.split(),
            "nb_pieces": self.nb_pieces,
            "pieces": chess.Board(self.fen).piece_map()}
