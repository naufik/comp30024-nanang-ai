from nanang.agent.searchtree import SearchTree
from nanang.game.board import Board
from nanang.game.move import Move
from math import inf

class Minimax3Tree(SearchTree):

  def __init__(self, root, color, expansion_depth, eval_f):
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
  
  def next_best(self):
    best_eval = -inf
    best_move = None
    
    for edge in self._root.possible_moves(self._color):
      self._mmthresh = best_eval
      edge_eval = self.eval_edge(edge)
      if edge_eval > best_eval:
        best_move = edge
        best_eval = edge_eval

    self._mmthresh = -inf
    if best_move is None:
      best_move = ("PASS", None)
    else:  
      self.set_root(self._root.possible_board(best_move))
      
    return best_move
    
  
  def eval_node(self, node):
    return self._eval(self._color, node)
  
  def eval_edge(self, edge):
    board_next = self._root.possible_board(edge)

    #gives the next player whose turn it is to play, given the current player's turn
    next_player = Board.next_player(self._color)
    thresh = self._mmthresh if self._mmthresh > -inf else None

    # evaluate a single "layer" of minimax search (a single layer here is
    # equivalent to three layers since we have three players!)
    return self._eval_minimax_layer(board_next, next_player, thresh)

  def _eval_minimax_layer(self, board, player, threshold=None):
    # try to re implement iteratively instead of recursively to save time.
    # TODO: add memoization.

    if (player == self._color):
      moves = board.possible_moves(player)
      return max([self.eval_node(board.possible_board(move)) for move in moves] + [0])
    else:
      moves = board.possible_moves(player)
      evals_min = None

      #for all possible moves by enemy
      for move in moves:
        next_board = board.possible_board(move)

        # we expand the board.
        # self._tree[board].append(next_board)
        measure = self._eval_minimax_layer(next_board,
          Board.next_player(player), evals_min)

        if evals_min is None or evals_min > measure:
          evals_min = measure
          if threshold is not None and evals_min <= threshold:
            # We know the worst possible case is going to be bad anyway
            return evals_min
      return evals_min
        
      