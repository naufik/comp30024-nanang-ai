class SearchTree:
  """
  This class represents a standard looking search tree. Where the tree is stored
  as a dictionary.

  The most important function here is the 'next' function which returns the next
  move that appears to be the best move after looking at the evaluation function
  on states of the search tree. 
  """

  import game.board
  import game.move

  def __init__(self, root):
    self._tree = {root: []}
    self._root = root
    self._queue = []
  # Internal representation of the tree.

  def next(self):
    # returns the next best move to make (via a generator) should update the
    # search tree as well.

    return None 

  def set_root(self, new_root):
    # sets the root of the tree to the new root.
    pass

  def eval_move(self, move):
    # evaluates a single move.
    pass
  
  def eval_board(self, board):
    # evaluates the board.
    pass