import random
from sqlalchemy import and_, func

from app.models import Puzzle


def get_puzzle(elo_min, elo_max, n_pieces_min, n_pieces_max):
    puzzle = Puzzle.query.filter(and_(
        Puzzle.division == random.randint(0, 99),
        Puzzle.elo >= elo_min,
        Puzzle.elo <= elo_max,
        Puzzle.nb_pieces >= n_pieces_min,
        Puzzle.nb_pieces <= n_pieces_max
    )).order_by(func.random()).first()
    res = puzzle.dict()
    res["total"] = len(Puzzle.query.all())
    return res if puzzle else {}
