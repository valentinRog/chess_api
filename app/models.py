import csv
import chess
from hashlib import sha256

from flask_sqlalchemy import SQLAlchemy

from .views import app


db = SQLAlchemy(app)

def init_tables():
    db.drop_all()
    db.create_all()
    db.session.commit()

class Puzzle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    division = db.Column(db.Integer(), index=True,
                         unique=False, nullable=False)
    elo = db.Column(db.Integer(), unique=False, nullable=False)
    fen = db.Column(db.String(200), unique=False, nullable=False)
    moves = db.Column(db.String(500), unique=False, nullable=False)
    nb_pieces = db.Column(db.Integer(), unique=False, nullable=False)

    def get_fens(self):
        board = chess.Board(self.fen)
        fens = [board.fen()]
        for move in self.moves.split():
            board.push_uci(move)
            fens.append(board.fen())
        return fens

    def get_boards(self):
        return map(lambda fen: chess.Board(fen), self.get_fens())

    def get_san_moves(self):
        return [board.san(board.parse_uci(move)) for board, move in zip(self.get_boards(), self.moves.split())]

    def get_legal_moves(self):
        legal_moves = []
        for board in self.get_boards():
            legal_moves.append([board.san(move) for move in board.legal_moves])
        return legal_moves

    def get_pieces(self):
        return {k: v.symbol() for k, v in chess.Board(self.fen).piece_map().items()}

    def __iter__(self):
        for key, value in {
            "id": self.id,
            "elo": self.elo,
            "fen": self.fen,
            "fen": self.get_fens(),
            "uci_moves": self.moves.split(),
            "san_moves": self.get_san_moves(),
            "legal_moves": self.get_legal_moves(),
            "nb_pieces": self.nb_pieces,
            "pieces": self.get_pieces()
        }.items():
            yield (key, value)

    N_CHUNKS = 100
    @classmethod
    def fill_from_csv(cls, stream, buffer_size=10_000):
        reader = csv.DictReader(stream)
        for row in reader:
            puzzle = cls(
                id = reader.line_num,
                division=int(sha256(row["FEN"].encode(
                    "utf-8")).hexdigest(), 16) % cls.N_CHUNKS,
                elo=int(row["Rating"]),
                fen=row["FEN"],
                moves=row["Moves"],
                nb_pieces=len(chess.Board(row["FEN"]).piece_map()))
            db.session.add(puzzle)
            if not (reader.line_num - 1) % buffer_size:
                db.session.commit()
                print(reader.line_num - 1, "puzzles added", end="\r")
        db.session.commit()
        print(reader.line_num - 1, "puzzles added")
