from nanang.agent.searchtree import SearchTree
from math import sqrt, log

# Thinking of storing the tree as (parent, node, Qscore, NScore, successors)
# Author's note: I JUST REALIZED A MONTE CARLO SEARCH TREE IS LITERALLY
# DR STRANGE!!! You look at a large enough number of possible futures and
# see how many times you would win...


class MonteCarloNode:
  exp_factor = 1.41259

  def __init__(self, parent, board):
    self.parent = parent
    self.board = board
    self.successors = []
    self.qscore = 0
    self.nscore = 0
  
  def explore(self):
    # TODO: continue this, should insert a random child to the tree.
    self.successors.append()
  
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
  

class MonteCarloSearchTree(SearchTree):
  def __init__(self, color, sim_count=5, max_depth=None, backup_eval=None):
    """
    Creates a Monte-Carlo search-tree to be implemented by the Player
    :param color: The color of the player utilizing the tree.
    :param sim_count: The number of simulations for the purposes of
    node-exploration. Bigger is slower.
    :param max_depth: The maximum depth of the simulation, naturally this is None
    so the MCTS will keep on simulating until a terminal state.
    :param backup_eval: Backup evaluation function when a maximum depth is given.
    """
    pass


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

  
