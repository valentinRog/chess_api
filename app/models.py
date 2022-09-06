import csv
import chess
import random
import pandas
import io

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from .views import app


db = SQLAlchemy(app)


def init_tables():
    db.drop_all()
    db.create_all()
    db.session.commit()


class Puzzle(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fen = db.Column(db.String(200), unique=False, nullable=False)
    elo = db.Column(db.Integer(), index=True, unique=False, nullable=False)
    moves = db.Column(db.String(500), unique=False, nullable=False)
    n_pieces = db.Column(
        db.Integer(),
        index=True,
        unique=False,
        nullable=False
    )

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

    def get_legal_uci_moves(self):
        return [[board.uci(move) for move in board.legal_moves] for board in self.get_boards()]

    def get_legal_san_moves(self):
        return [[board.san(move) for move in board.legal_moves] for board in self.get_boards()]

    def get_pieces(self):
        return {k: v.symbol() for k, v in chess.Board(self.fen).piece_map().items()}

    def __iter__(self):
        for key, value in {
            "elo": self.elo,
            "fen": self.fen,
            "fens": self.get_fens(),
            "uci_moves": self.moves.split(),
            "san_moves": self.get_san_moves(),
            "legal_uci_moves": self.get_legal_uci_moves(),
            "legal_san_moves": self.get_legal_san_moves(),
            "n_pieces": self.n_pieces,
            "pieces": self.get_pieces()
        }.items():
            yield (key, value)

    @classmethod
    def fill_from_csv(cls, infile, buffer_size=10_000):
        Puzzle.query.delete()
        df = pandas.read_csv(infile, usecols=["FEN", "Rating", "Moves"])
        df = df.sample(frac=1)
        stream = io.StringIO()
        df.to_csv(stream, sep=",", index=False)
        reader = csv.DictReader(io.StringIO(stream.getvalue()))
        for row in reader:
            puzzle = cls(
                id=reader.line_num,
                fen=row["FEN"],
                elo=int(row["Rating"]),
                moves=row["Moves"],
                n_pieces=len(chess.Board(row["FEN"]).piece_map()))
            db.session.add(puzzle)
            if not reader.line_num % buffer_size:
                db.session.commit()
                print(reader.line_num, "puzzles added", end="\r")
        db.session.commit()
        print(reader.line_num, "puzzles added")

    @classmethod
    def get_random(cls, elo_min=0, elo_max=4000, n_pieces_min=0, n_pieces_max=32):
        id_range = (1, cls.query.order_by(cls.id.desc()).first().id)
        target_id = random.randint(*id_range)
        if target_id < sum(id_range) / 2:
            puzzle = cls.query.filter(and_(
                cls.id >= target_id,
                cls.elo >= elo_min,
                cls.elo <= elo_max,
                cls.n_pieces >= n_pieces_min,
                cls.n_pieces <= n_pieces_max
            )).order_by(cls.id.asc()).first()
        else:
            puzzle = cls.query.filter(and_(
                cls.id <= target_id,
                cls.elo >= elo_min,
                cls.elo <= elo_max,
                cls.n_pieces >= n_pieces_min,
                cls.n_pieces <= n_pieces_max
            )).order_by(cls.id.desc()).first()
        return dict(puzzle)
