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

	def __init__(self, id, elo, fen, moves, nb_pieces):
		self.id = id
		self.elo = elo
		self.fen = fen
		self.moves = moves
		self.nb_pieces = nb_pieces


def init_db():
	db.drop_all()
	db.create_all()
	with open('debug_puzzles.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			puzzle = Puzzle(reader.line_num, int(row["Rating"]), row["FEN"], row["Moves"], len(chess.Board(row["FEN"]).piece_map()))
			db.session.add(puzzle)
			if not reader.line_num % 10000:
				db.session.commit()
		db.session.commit()