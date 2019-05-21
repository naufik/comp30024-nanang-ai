from nanang.agent.searchtree import SearchTree
from nanang.game.board import Board
from nanang.game.move import Move
from math import inf
from sys import stderr
import cProfile

class Minimax3Tree(SearchTree):

  def __init__(self, root, color, expansion_depth, eval_f, **kwargs):
    """
    Initializes a minimax search tree.
    :param root: the root of the tree.
    :param color: the color of the player in using this tree.
    :param expansion_depth: the depth of the expansion of the tree on a single
    search.
    :param eval_f: the evaluation function used to evaluate a single board,
    needs to be in callable with two arguments - where the first argument is the
    color and the second argument is the board.
    """
    SearchTree.__init__(self, root)
    self._color = color
    self._xdepth = expansion_depth
    self._eval = eval_f
    self._random = None

    if kwargs["random"] == True:
      self._random = {}
      self._random["chance"] = kwargs["chance"]
      self._random["threshold"] = kwargs["threshold"]

  def next_best(self):
    best_eval = -inf
    best_move = None
    
    
    thing = self._eval_minimax_ab(self._root, self._color, depth=self._xdepth)
    # cProfile.runctx("tt()", locals(), globals())
    return thing[1], thing[0]
    
  
  def eval_node(self, node):
    return self._eval(self._color, node)[0]

  def eval_edge(self, edge):
    board_next = self._root.possible_board(edge)

    #gives the next player whose turn it is to play, given the current player's turn
    next_player = Board.next_player(self._color)

    # evaluate a single "layer" of minimax search (a single layer here is
    # equivalent to three layers since we have three players!)
    return self._eval_minimax_ab(board_next, next_player, depth=self._xdepth)

  def _eval_minimax_ab(self, board: Board, player, alpha=-inf, beta=inf, depth=1):
    """
    Performs a minimax adversarial search, algorithm implementation is based on
    psuedocode in https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning.
    :param board: the root of the search
    :param player: color of the maximizing player, either "R", "G", "B".
    :param depth: the depth of the search, depth 0 will only give evaluation
    function of the root.
    """

    if depth == 0:
      evalue = 0.0
      if board.get_winner() == self._color:
        evalue = inf
      elif board.pieces_of(self._color) == 0:
        evalue = -inf
      else:
        evalue = self.eval_node(board)

      return (evalue, None) 
    else:
      if player == self._color:
        value = -inf
        best_move = None
        for move in board.possible_moves(player):
          value = max(value, self._eval_minimax_ab(board.possible_board(move),
            Board.next_player(player), alpha, beta, depth-1)[0])
          if best_move is None or value > alpha:
            alpha = value
            best_move = move
          if alpha > beta:
            break
        return value, best_move
      else:
        value = inf
        best_cuck = None
        for move in board.possible_moves(player):
          value = min(value, self._eval_minimax_ab(board.possible_board(move),
            Board.next_player(player), alpha, beta, depth-1)[0])
          if best_cuck is None or value <= beta:
            beta = value
            best_cuck = move
          if alpha > beta:
            break
        return value, best_cuck
        
      