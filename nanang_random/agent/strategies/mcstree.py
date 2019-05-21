from pantat_bohAI.agent.searchtree import SearchTree
from pantat_bohAI.game.board import Board
from pantat_bohAI.game.move import Move
from math import sqrt, log
from random import SystemRandom

# Thinking of storing the tree as (parent, node, Qscore, NScore, successors)
# Author's note: I JUST REALIZED A MONTE CARLO SEARCH TREE IS LITERALLY
# DR STRANGE!!! You look at a large enough number of possible futures and
# see how many times you would win...

class MonteCarloNode:
  exp_factor = 1.41259

  def __init__(self, parent, board, move_from=None):
    self.parent = parent
    self.board = board
    self.successors = []
    self.qscore = 0
    self.nscore = 0
    self._memoized_moves = None
    self._transition = move_from
  
  def explore(self):
    if self._memoized_moves is None:
      self._memoized_moves = self.board.possible_moves(self.board.current_turn)
    
    assert(len(self._memoized_moves) > 0)

    index = MonteCarloSearchTree.rng.randint(0, len(self._memoized_moves) - 1)
    
    # select a random move
    move = self._memoized_moves.pop(index)

    new_node = MonteCarloNode(self, 
      self.board.possible_board(move), move_from=move)

    self.successors.append(new_node)
    return new_node
    
  
  def propagate_up(self, winner):
    self.nscore += 1
    self.qscore += int(self.board.current_turn == winner)
    if self.parent is not None:
      self.parent.propagate_up(winner)

  def node_eval(self):
    if (self.nscore == 0) or (self.parent is None):
      return 0
    return (self.qscore / self.nscore) + \
      MonteCarloNode.exp_factor * sqrt(log(self.parent.nscore) / self.nscore)
  
  def __eq__(self, other):
    return self.board == other.board
  
  def __hash__(self):
    return hash(self.board)

class MonteCarloSearchTree(SearchTree):
  rng = SystemRandom()

  def __init__(self, root, color, sim_count=100, max_depth=None, backup_eval=None):
    """
    Creates a Monte-Carlo search-tree to be implemented by the Player
    :param color: The color of the player utilizing the tree.
    :param sim_count: The number of simulations for the purposes of
    node-exploration. Bigger is slower.
    :param max_depth: The maximum depth of the simulation, naturally this is None
    so the MCTS will keep on simulating until a terminal state.
    :param backup_eval: Backup evaluation function when a maximum depth is given.
    """
    super().__init__(root)
    self.color = color
    self._sim = sim_count
    self._maxdepth = max_depth
    self.backup_eval = backup_eval
    self._master_turn_count = 0
    self.tree_set = set()
    self._mct_root = None
    self.set_root(root)



  # Override
  def set_root(self, new_root):
    super().set_root(new_root)
    
    x_node = self.find_in_set(new_root)
    if x_node is not None:
      self._mct_root = x_node
    else:
      self._mct_root = MonteCarloNode(self._mct_root, new_root)
      self.tree_set.add(self._mct_root)
    
    if (new_root.current_turn == self.color):    
      self._master_turn_count += 1

  def find_in_set(self, board):
    for node in self.tree_set:
      if node.board == board:
        return node
    return None

  def next_best(self):
    self.monte_carlo_fullsearch()
    if len(self._mct_root.successors) == 0:
      return Move(self.color, None, None)
    else:
      candidate = max(self._mct_root.successors, key=lambda n: n.nscore)
      return candidate._transition


  def monte_carlo_fullsearch(self):
    for _ in range(self._sim):
      # Selection and Expansion
      expand = self.monte_carlo_select(self._mct_root)
      new_node = expand.explore()
      self.tree_set.add(new_node)

      win = self.monte_carlo_simulate(new_node)

      new_node.propagate_up(win)

  def monte_carlo_select(self, node: MonteCarloNode):
    return_node = node

    if (node._memoized_moves is None) or (len(node._memoized_moves) > 0):
      return return_node
    
    if node.successors != []:
      max_node = self.monte_carlo_select(max(node.successors, 
        key=MonteCarloNode.node_eval))

      return max_node

    return return_node
  
  def monte_carlo_simulate(self, node):
    board: Board = node.board
    turn_counter = self._master_turn_count
    player_begin = board.current_turn

    while board.get_winner() is None:
      if turn_counter >= 256:
        break

      moves = board.possible_moves(board.current_turn)
      index = MonteCarloSearchTree.rng.randint(0, len(moves) - 1)
      board.make_move(moves[index])
      
      if board.current_turn == player_begin:
        turn_counter += 1  
    
    winner = board.get_winner()
    if winner is not None:
      return winner
    else:
      # draw mechanism, right now do a weighted three-player coin flip.
      return "RGB"[MonteCarloSearchTree.rng.randint(0, 2)]
    

  
