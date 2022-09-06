from flask import render_template
from string import ascii_lowercase, ascii_uppercase

from .app import app
from .models import Puzzle


@app.route("/", defaults={"level": 0})
@app.route("/<int:level>")
def index(level):
    puzzle = Puzzle.get_random()
    pieces = {
        "white": {k: v for k, v in puzzle["pieces"].items() if k in ascii_uppercase},
        "black": {k: v for k, v in puzzle["pieces"].items() if k in ascii_lowercase}
    }
    return render_template(
        "index.html",
        puzzle=puzzle,
        pieces=pieces
    )
