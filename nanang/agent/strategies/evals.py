"""
A collection of well defined evaluation functions.
"""

from nanang.game.board import Board
from nanang.game.move import Move
from random import SystemRandom
from math import inf

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



def eval_one(color, board: Board, weights=[500, 250, 50000000, 200, 200]):
  features = []
  h0 = 0
  others = {"R", "G", "B"} - {color}

  feature1 = len(board.pieces_of(color))
  features.append(feature1)


  feature2 = -sum(len(board.pieces_of(c)) for c in others)
  features.append(feature2)

  feature3 = board._win_state[color]
  features.append(feature3)

  feature4 = -mn_dist(color, board)
  features.append(feature4)

  feature5 = sum([0] + [mn_dist(x, board) for x in others])
  features.append(feature5)

  for i in range(len(features)):
    h0 += weights[i] * features[i]

  return h0, features

def eval_one_b(color, board, weights):
  others = {"R", "G", "B"} - {color}
  features = []
  feature1 = 4 + (len(board.pieces_of(color))-4) * 0.2
  features.append(feature1)


  feature2 = -sum(len(board.pieces_of(c)) for c in others) * 0.5
  features.append(feature2)

  feature3 = board._win_state[color] * 2
  features.append(feature3)

  feature4 = -mn_dist(color, board) * 3
  features.append(feature4)

  feature5 = sum([0] + [mn_dist(x, board) for x in others]) * 0.5
  features.append(feature5)
  
  h0 = 0.0
  for i in range(len(features)):
    h0 += features[i] * weights[i]

  return h0, features

WEIGHTS_PAR=[500.0004037109066,249.9992955679865,5000.0,199.99923005056738,199.99923005056738]

def eval_two(color, board, weights):
  if len(board.pieces_of(color)) + board._win_state[color] <= 4:
    return eval_one(color, board, weights)
  else:
    return eval_one_b(color, board, weights)

rng = SystemRandom()
def best_eval_ever(color, board: Board):
  return rng.randint(-3000, 3000), [1]


DEFAULT_WEIGHTS = [rng.randint(-100,100) for i in range(2750)]
def linear_reg_eval(color, board: Board, weights=DEFAULT_WEIGHTS):
  features = []
  COORDS = sorted(board._dict_rep.keys())
  # print(COORDS)

  h0 = 0.0
  others = {"R","G","B"} - {color}
  for point in COORDS:
    features.append(int(board._dict_rep[point] == color))
  for point in COORDS:
    features.append(int(board._dict_rep[point] in others))
  
  for c in range(len(COORDS)):
    for point2 in COORDS[c+1:]:
      point = COORDS[c]
      if point != point2:
        # allied interaction
        features.append(int(board._dict_rep[point] == color) * \
          int(board._dict_rep[point2] == color))

        # crossed interaction
        features.append(int(board._dict_rep[point] == color) * \
          int(board._dict_rep[point2] in others))
        features.append(int(board._dict_rep[point2] == color) * \
          int(board._dict_rep[point] in others))
        
        # enemy interaction
        features.append(int(board._dict_rep[point] in others) * \
          int(board._dict_rep[point2] in others))

  features.append(len(board.pieces_of(color)))
  features.append(board._win_state[color])
  
  for i in range(len(features)):
    h0 += weights[i] * features[i]
  return h0, features

