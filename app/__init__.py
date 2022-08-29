from flask import Flask
import atexit

from .views import app
from . import models
from .init_db import init_db

models.db.init_app(app)
init_db()
