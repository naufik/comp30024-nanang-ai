class SearchTree:
  """
  This class represents a standard looking search tree. Where the tree is stored
  as a dictionary.

  The most important function here is the 'next' function which returns the next
  move that appears to be the best move after looking at the evaluation function
  on states of the search tree. 
  """
  from game.board import Board
  from game.move import Move

  def __init__(self, root: Board):
    self._tree = {root: []}
    self._root = root

  def next(self):
    # returns the next best move to make (via a generator) should update the
    # search tree as well.
    return None

  def set_root(self, new_root):
    self._tree[self._root].append(new_root)
    self._root = new_root
    if new_root not in self._tree:
      self._tree[new_root] = []

  def eval_move(self, move):
    # evaluates a single move - default assumes uniform evaluation of moves.
    return 1
  
  def eval_board(self, board):
    # evaluates a single board - default assumes uniform evaluation of boards.
    return 1