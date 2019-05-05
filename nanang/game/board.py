"""
A representation of a board. The following things need to be implemented.

This has nothing yet, except for skeleton for all the things that we need to
implement.

A piece has a 'controller' and a 'position', the 'controller' is the team that
controls a piece, which is a selection of 'R', 'G', 'B', 'X'. ('X' refers to the
blocking pieces.)
"""
from game.move import Move

class Board:
  _turn_dict = {"R": "G", "G": "B", "B": "R"}

  @staticmethod
  def next_player(color):
    return Board._turn_dict[color]

  @staticmethod
  def empty_board_dict():
    # creates an empty board dictionary.
    board_dict = dict()
    ran = range(-3, 4)    
    
    for cell in [(q,r) for q in ran for r in ran if -q-r in ran]:
      board_dict[cell] = None

    return board_dict

  @staticmethod
  def initialize_board(self):
    red = [[-3, 0], [-3, 1], [-3, 2], [-3, 3]]
    blue = [[3, 0], [2, 1], [1, 2], [0, 3]]
    green = [[0, -3], [1, -3], [2, -3], [3, -3]]

    # initialize empty board
    pieces_coors = {"R": red, "B": blue, "G": green}
    board_dict = Board.empty_board_dict()
    for key, coors in pieces_coors.items():
      for coor in coors:
        point = (coor[0], coor[1])
        if (point in board_dict):
          board_dict[point] = key
        else:
          raise IndexError

    return board_dict

  def __init__(self, board_dict, winner_dict=None, current="R", debug=False):
    # The dictionary representation of the board.
    self._dict_rep = board_dict
    if winner_dict is None:
      winner_dict = {"R": 0, "G": 0, "B": 0}
    self._win_state = winner_dict
    self.debug = debug
    self.current_turn = current

  @staticmethod
  def piece_goal(self, key, pos):
    #checks if a position is a goal position for a specific key. 
    if key == "R":
      return pos[0] == 3
    elif key == "G":
      return pos[1] == 3
    elif key == "B":
      return pos in {(0,-3), (-1, -2), (-2, -1), (-3, 0)}

  def possible_moves(self, controller, pieces_pos=None):
    if (pieces_pos is None):
      #if a piece list is supplied, take their word for it
      pieces_pos = self.pieces_of(controller)

    moves = []
    for pos in pieces_pos:
      moves.extend([Move(controller, pos, x) for x in   \
        map(lambda i: (pos[0] + i[0], pos[1] + i[1]), 
        Move.DELTAS_JUMP + Move.DELTAS_MOVE) if Move._in_board(x)])
      
      try:
        # really hackish way to consider the exit moves, may change later.
        moves.append(Move(controller, pos, None))
      except AssertionError:
        pass
    
    return list(filter(lambda move: self.valid_move(move), moves))

  def pieces_of(self, controller):
    assert(controller in ["R", "G", "B"])
    pieces = []
    for key in self._dict_rep:
      if self._dict_rep[key] == controller:
        pieces.append(key)
    return pieces

  def valid_move(self, move: Move):
    """
    Checks if a move is valid
    """
    if move.controller != self.current_turn:
      return False

    if move._exitable():
      return self._dict_rep[move.source] == move.controller
    elif move._adjacent():
      return (self._dict_rep[move.source] == move.controller \
        and self._dict_rep[move.dest] == None)
    elif move._jumpable():
      mid = tuple([(a+b)//2 for a,b in zip(move.dest, move.source)])
      return (self._dict_rep[move.source] == move.controller and
        self._dict_rep[move.dest] is None and
        self._dict_rep[mid] is not None)
    
  def make_move(self, move):
    """
      Alters the state of the board, as if we have performed the move described
      in the argument move.
    """
    if (self.valid_move(move)):
      new_board = self.possible_board(move)
      self._dict_rep = new_board._dict_rep
      self._win_state = new_board._win_state
      print(str(move))
      return True
    return False
  
  def possible_board(self, move: Move):
    """
      Returns a board state after as if we performed this move, this method is
      best used only for searching.

      @naufik: I'm a bit concerned about the search using too much memory if
      we're using objects because of the overhead tbh. But this makes writing
      the code easier later on as you can just chain this method.
    """
    assert(self.valid_move(move))
    dst = move.dest
    src = move.source
    new_dict = self._dict_rep.copy()
    new_winners = self._win_state.copy()

    if dst is not None:
      if move._jumpable():
        mid = tuple([(a+b)//2 for a,b in zip(move.dest, move.source)])
        new_dict[mid] = new_dict[src]
      new_dict[dst] = new_dict[src]
      new_dict[src] = None
    else:
      new_dict[src] = None
      
    return Board(new_dict, winner_dict=new_winners, 
      current=Board.next_player(self.current_turn), debug=self.debug)


  def __eq__(self, other):
    """
      Returns True if the board self and other are "equal in state", and False
      otherwise.

      Note: this overloads the == operator, allowing you to write board1 == board2
      to make a call to this method. Fuck Java for not having this.
    """
    return self._dict_rep == other._dict_rep

  def __str__(self):
    return self._stringify_board(debug=self.debug)

  def __hash__(self):
    return hash(tuple(sorted(self._dict_rep.items())))

  def _stringify_board(self, message="", debug=False):
    # Adapted from the sample code given
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in self._dict_rep:
            cell = str(self._dict_rep[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    return board
  
  def as_dict(self, other):
    """
    Returns the dictionary representation of the board.
    """
    return dict(self._dict_rep.entries())

  def __lt__(self, other):
    return False