from flask import render_template
from .app import app

from .models import Puzzle


@app.route('/')
def index():
    return render_template(
        "index.html",
        puzzle=Puzzle.get_random()
    )
