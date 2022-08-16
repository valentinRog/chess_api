from flask import jsonify
from .app import app

from . import puzzle


@app.route('/')
def index():
    return '<h1>Yo</h1>'


@app.route("/get_puzzle/<int:elo_min>/<int:elo_max>/<int:n_pieces_min>/<int:n_pieces_max>")
def get_puzzle(elo_min, elo_max, n_pieces_min, n_pieces_max):
    return jsonify(puzzle.get_puzzle(elo_min, elo_max, n_pieces_min, n_pieces_max))
