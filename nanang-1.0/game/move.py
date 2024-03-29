"""

"""

_bran = range(-3, +3+1)

class Move:
  DELTAS_MOVE = [ (0, 1), (0, -1), (1, -1), (-1, 1), (-1, 0), (1,0) ]
  DELTAS_JUMP = [ (0, 2), (0, -2), (2, -2), (-2, 2), (2, 0), (-2, 0) ]
  
  BOARD_RANGE = [(q,r) for q in _bran for r in _bran if -q-r in _bran]

  @staticmethod
  def _in_board(point):
    return point in Move.BOARD_RANGE

  def __init__(self, controller, source, dest):
    self.source = source
    self.controller = controller
    self.dest = dest
    if dest != None:
      assert(Move._in_board(source) and Move._in_board(dest))
      assert(self._jumpable() or self._adjacent())
    else:
      assert(self._exitable())

  def _exitable(self):
    if (self.dest == None):
      if self.controller == "R":
        return self.source[0] == 3
      elif self.controller == "G":
        return self.source[1] == 3
      elif self.controller == "B":
        return self.source in [(0,-3), (-1, -2), (-2, -1), (-3, 0)]
    return False

  def _adjacent(self):
    delta = (self.dest[0] - self.source[0], self.dest[1] - self.source[1])
    return delta in Move.DELTAS_MOVE

  def _jumpable(self):
    if (self.dest is None):
      return False
    delta = (self.dest[0] - self.source[0], self.dest[1] - self.source[1])
    return delta in Move.DELTAS_JUMP

  def __str__(self):
    if self.dest == None:
      return f"EXIT from {self.source}."
    elif self._adjacent():
      return f"MOVE from {self.source} to {self.dest}."
    elif self._jumpable():
      return f"JUMP from {self.source} to {self.dest}."
    else:
      return f"# something went wrong"

  def __hash__(self):
    return hash((self.controller, self.source, self.dest))