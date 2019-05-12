from nanang.agent.searchtree import SearchTree
from nanang.game.board import Board
from math import sqrt, log
from random import SystemRandom

# Thinking of storing the tree as (parent, node, Qscore, NScore, successors)
# Author's note: I JUST REALIZED A MONTE CARLO SEARCH TREE IS LITERALLY
# DR STRANGE!!! You look at a large enough number of possible futures and
# see how many times you would win...

class MonteCarloNode:
  exp_factor = 1.41259

  def __init__(self, parent: MonteCarloNode, board: Board):
    self.parent = parent
    self.board = board
    self.successors = []
    self.qscore = 0
    self.nscore = 0
  
  def explore(self, color):
    # TODO: continue this, should insert a random child to the tree.
    possible_moves = self.board.possible_moves(color)
    index = MonteCarloSearchTree.rng.randint(0, len(possible_moves) - 1)

    new_node = MonteCarloNode(self, 
      self.board.possible_board(possible_moves[index]))

    self.successors.append(new_node)
    return new_node
    
  
  def propagate_up(self, positive):
    self.nscore += 1
    self.qscore = int(positive)
    if self.parent is not None:
      self.parent.backtrack(positive)

  def node_eval(self):
    if self.nscore == 0:
      return 0
    return (self.qscore / self.nscore) + \
      MonteCarloNode.exp_factor * sqrt(log(self.qscore) / self.nscore)
  
  def __eq__(self, other):
    return self.board == other.board
  
  def __hash__(self):
    return self.board.__hash__()

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
    self.color = color
    self._sim = sim_count
    self._maxdepth = max_depth
    self.backup_eval = backup_eval
    self.set_root(root)

    self.tree_set = set()

  # Override
  def set_root(self, new_root):
    super().set_root(new_root)
    
    x_node = self.find_in_set(new_root)
    if x_node is not None:
      self._mct_root = x_node
    else:
      new_node = MonteCarloNode(self._mct_root, new_root)
      self.tree_set.add(new_node)
    

  def find_in_set(self, board):
    for node in self.tree_set:
      if node.board == board:
        return node
    return None


  def next_best(self):
    pass
  
  def eval_node(self, node):
    pass
  
  def eval_edge(self, node):
    pass

  def monte_carlo_select(self, node):
    pass
  
  def monte_carlo_simulate(self, node):
    pass

  def monte_carlo_update(self, node, score):
    pass

  
