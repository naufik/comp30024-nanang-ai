from agent.searchtree import SearchTree
from game.board import Board
from game.move import Move

class Minimax3Tree(SearchTree):

  def __init__(self, root, color, expansion_depth, eval_f, 
    eval_f2=lambda x: -eval_f(x)):
    
    SearchTree.__init__(root)
    self._color = color
    self._xdepth = expansion_depth
    self._eval = eval_f
  
  def next_best(self):
    return sorted([edge for edge in self._root.possible_moves(self._color)],
      key = self.eval_edge)[0]
    
  
  def eval_node(self, node):
    return self._eval(node)
  
  def eval_edge(self, edge):
    board_next = self._root.possible_board(edge)
    next_player = Move.next(self._color)

    # evaluate a single "layer" of minimax search (a single layer here is
    # equivalent to three layers since we have three players!)
    return self._eval_minimax_layer(board_next, next_player)

  def _eval_minimax_layer(self, board, player, threshold=None):
    # try to re implement iteratively instead of recursively to save time.
    # TODO: add memoization.

    if (player == self._color):
      moves = board.possible_moves(player)
      return max([self.eval_node(board.possible_board(move)) for move in moves])
    else:
      moves = board.possible_moves(player)
      evals_min = None
      move_min = None

      for move in moves:
        measure = self._eval_minimax_layer(board.possible_board(move),
          Board.next_player(player), evals_min)

        if evals_min is None or evals_min > measure:
          evals_min = measure
          move_min = move
          if threshold is not None and evals_min <= threshold:
            # We know the worst possible case is going to be bad anyway
            return evals_min
      return evals_min
        
      