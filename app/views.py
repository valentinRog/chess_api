from flask import jsonify, render_template
from .app import app

from . import puzzle


@app.route('/')
def index():
    return render_template(
        "index.html",
        puzzle=puzzle.get_puzzle(0, 3000, 0, 32))


@app.route("/get_puzzle/<int:elo_min>/<int:elo_max>/<int:n_pieces_min>/<int:n_pieces_max>")
def get_puzzle(elo_min, elo_max, n_pieces_min, n_pieces_max):
    return jsonify(puzzle.get_puzzle(elo_min, elo_max, n_pieces_min, n_pieces_max))
