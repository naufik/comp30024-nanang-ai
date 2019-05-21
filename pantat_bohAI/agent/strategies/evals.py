"""
A collection of well defined evaluation functions.
"""

from pantat_bohAI.game.board import Board
from pantat_bohAI.game.move import Move
from random import SystemRandom

GOALS = {        
  "R": [(3, -3), (3, -2), (3, -1), (3, 0)],
  "G":  [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
  "B":  [(0, -3), (-1, -2), (-2, -1), (-3, 0)]
}

def _dist(x, y):
  return max(x[0]-y[0], x[1]-y[1], (-x[0]-x[1])-(-y[0]-y[1]))

def mn_dist(colour, board: Board):
  """
  function calculates the sorted sum of minimum distances between a player and their nearest goals.
  A goal tile being the exit tiles for a particular colour.
  :param colour: the player's colour for which the distance will be analayzed for
  :param board: the current state of the board
  :return:
  """
  pieces = board.pieces_of(colour)
  return sum(sorted([_dist(piece, goal) for goal in GOALS[colour] for piece in pieces])[:4])



def main_eval(colour, board: Board, weights=[500, 250, 50000000, 200, 200]):
  """
  the main evaluation function to be used byb the agent
  :param colour: the player's colour for which the evaluation function is being calculated for
  :param board: the board for which the evaluation function is to be evaluated on
  :param weights: the weights given to each feature
  :return: the value of the evaluation function and an array of the features used by it
  """

  features = []
  h0 = 0
  others = {"R", "G", "B"} - {colour}

  #the number of ally pieces that are within the board and that have exited the board
  feature1 = len(board.pieces_of(colour)) + board._win_state[colour]
  features.append(feature1)

  #the number of enemy pieces within the board
  feature2 = -sum(len(board.pieces_of(c)) for c in others)
  features.append(feature2)

  #the number of ally pieces that have exited the game
  feature3 = board._win_state[colour]
  features.append(feature3)

  #the sum of minimum distances between all ally pieces that have exited the game
  feature4 = -mn_dist(colour, board)
  features.append(feature4)

  #the sum of minimum distances between all enemy pieces to their respective nearest goals
  feature5 = sum([0] + [mn_dist(x, board) for x in others])
  features.append(feature5)

  for i in range(len(features)):
    h0 += weights[i] * features[i]

  return h0, features

def win_eval(colour, board, weights):
  """
  the evaluation function for a win-priority strategy
  :param colour: the player's colour for which the evaluation function is being calculated for
  :param board: the board for which the evaluation function is to be evaluated on
  :param weights: the weights given to each feature
  :return: the value of the evaluation function and an array of the features used by it
  """
  others = {"R", "G", "B"} - {colour}
  features = []
  h0 = 0.0

  #the number of ally pieces that are within the board and that have exited the board
  feature1 = len(board.pieces_of(colour)) * 0.75 + board._win_state[colour]
  features.append(feature1)

  #the number of enemy pieces within the board
  feature2 = -sum(len(board.pieces_of(c)) for c in others)
  features.append(feature2)

  #the number of ally pieces that have exited the game
  feature3 = board._win_state[colour] * 2
  features.append(feature3)

  #the sum of minimum distances between all ally pieces that have exited the game
  feature4 = -mn_dist(colour, board) * 3
  features.append(feature4)

  #the sum of minimum distances between all enemy pieces to their respective nearest goals
  feature5 = sum([0] + [mn_dist(x, board) for x in others])
  features.append(feature5)

  for i in range(len(features)):
    h0 += features[i] * weights[i]

  return h0, features

WEIGHTS_PAR=[500.0004037109066,249.9992955679865,5000.0,199.99923005056738,199.99923005056738]

def meta_eval(colour, board, weights):
  """
  function handles dynamic evaluation, that is it manages the evaluation function for which the search tree will use
  to evaluate a state
  :param colour: the player's colour for which the evaluation function is being calculated for
  :param board: the board for which the evaluation function is to be evaluated on
  :param weights: the weights given to each feature
  :return: the evaluation function
  """
  if len(board.pieces_of(colour)) + board._win_state[colour] <= 4:
    return main_eval(colour, board, weights)
  else:
    return win_eval(colour, board, weights)

rng = SystemRandom()
def random_eval(colour, board: Board):
  """
  random evaluation function for the purposes of simulating a random agent
  :param colour: the player's colour for which the evaluation function is being calculated for
  :param board: the board for which the evaluation function is to be evaluated on
  :return: value of the evaluation function
  """
  return rng.randint(-3000, 3000), [1]


DEFAULT_WEIGHTS = [rng.randint(-100,100) for i in range(2750)]
def linear_reg_eval(colour, board: Board, weights=DEFAULT_WEIGHTS):
  features = []
  COORDS = sorted(board._dict_rep.keys())
  # print(COORDS)

  h0 = 0.0
  others = {"R","G","B"} - {colour}
  for point in COORDS:
    features.append(int(board._dict_rep[point] == colour))
  for point in COORDS:
    features.append(int(board._dict_rep[point] in others))
  
  for c in range(len(COORDS)):
    for point2 in COORDS[c+1:]:
      point = COORDS[c]
      if point != point2:
        # allied interaction
        features.append(int(board._dict_rep[point] == colour) * \
          int(board._dict_rep[point2] == colour))

        # crossed interaction
        features.append(int(board._dict_rep[point] == colour) * \
          int(board._dict_rep[point2] in others))
        features.append(int(board._dict_rep[point2] == colour) * \
          int(board._dict_rep[point] in others))
        
        # enemy interaction
        features.append(int(board._dict_rep[point] in others) * \
          int(board._dict_rep[point2] in others))

  features.append(len(board.pieces_of(colour)))
  features.append(board._win_state[colour])
  
  for i in range(len(features)):
    h0 += weights[i] * features[i]
  return h0, features


def interaction_eval(color, board, weights):
  others = {"R", "G", "B"} - {color}
  features = []

  pc = len(board.pieces_of(color))
  ws = board._win_state[color]

  adv_coef = int(pc + ws >= 5)
  # feature 1,2: pieces
  features.append(pc)
  # with coefficient
  features.append(pc * adv_coef)

  mnd = mn_dist(color,board)
  
  # feature 3,4: distance
  features.append(mnd)
  
  # with coefficient
  features.append(mnd * adv_coef)

  endist = sum([0] + [mn_dist(x, board) for x in others])
  # features 5,6 enemy distance
  features.append(endist)
  features.append(endist * adv_coef)

  # feature 7 the winning state
  features.append(ws)
  not_enough = int(pc + board._win_state[color] < 4)
  
  # this is the broken feature.
  # features.append(not_enough * ws)

  # thing
  # features.append(mnd * not_enough)

  ## problem: how the fuck do we get back into offense if we need to?
  h0 = sum([w * f for w, f in zip(weights, features)] + [0])
  return h0, features

