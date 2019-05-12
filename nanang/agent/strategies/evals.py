"""
A collection of well defined evaluation functions.
"""

from nanang.game.board import Board
from nanang.game.move import Move
from random import SystemRandom

GOALS = {        
  "R": [(3, -3), (3, -2), (3, -1), (3, 0)],
  "G":  [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
  "B":  [(0, -3), (-1, -2), (-2, -1), (-3, 0)]
}

def _dist(x, y):
  return max(x[0]-y[0], x[1]-y[1], (-x[0]-x[1])-(-y[0]-y[1]))

def mn_dist(color, board: Board):
  pieces = board.pieces_of(color)
  return sum(sorted([_dist(piece, goal) for goal in GOALS[color] for piece in pieces])[:4])

w = [500, 250, 2000, 200, 200]

def eval_one(color, board: Board):
  h0 = 0
  h0 += w[0] * len(board.pieces_of(color))
  others = {"R", "G", "B"} - {color}
  h0 -= w[1] * sum(len(board.pieces_of(c)) for c in others)
  h0 += w[2] * board._win_state[color]
  h0 -= w[3] * mn_dist(color, board)
  h0 += w[4] * sum([0] + [mn_dist(x, board) for x in others])
  return h0

rng = SystemRandom()
def best_eval_ever(color, board: Board):
  return rng.randint(-3000, 3000) + 50000 * board._win_state[color]

