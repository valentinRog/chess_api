from flask_sqlalchemy import SQLAlchemy
from .views import app

db = SQLAlchemy(app)

class Puzzle(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	elo = db.Column(db.Integer(), nullable=False)

db.create_all()