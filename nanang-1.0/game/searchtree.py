class SearchTree:
  
  def __init__(self, root):
    self._tree = {root}
    self._root = root
    self._queue = []
  # Internal representation of the tree.

  def next(self):
    # returns the next best move to make (via a generator)
    # this should update the search tree as well.
    pass

  def set_root(self, new_root):
    pass

  def queuing_function(self, new_root):
    pass

  def eval_move(self, move):
    pass

  def eval_board(self, board):
    pass