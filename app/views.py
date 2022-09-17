from flask import jsonify

from .app import app
from .models import Puzzle


@app.route("/")
def index():
    response = jsonify(Puzzle.get_random())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/level/<int:level>")
def level(level=1):
    min_limit = 2500
    elo_max = int(600 + 100 * (level / 3))
    elo_min = elo_max - 100
    if elo_min > min_limit:
        elo_min = min_limit
    n_pieces_max = int(4 + level / 2)
    response = jsonify(Puzzle.get_random(
        elo_min=elo_min,
        elo_max=elo_max,
        n_pieces_max=n_pieces_max
    ))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
