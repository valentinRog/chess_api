from flask import jsonify

from .app import app
from .models import Puzzle

@app.route("/")
def puzzle():
    response = jsonify(Puzzle.get_random())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
