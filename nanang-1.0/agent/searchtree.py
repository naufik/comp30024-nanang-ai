class SearchTree:
  """
  This class represents a standard looking search tree. Where the tree is stored
  as a dictionary.

  The most important function here is the 'next' function which returns the next
  move that appears to be the best move after looking at the evaluation function
  on states of the search tree. 
  """

  def __init__(self, root):
    self._tree = {root: []}
    self._root = root

  def next(self):
    # returns the next best move to make (via a generator) should update the
    # search tree as well.
    return self.expand_node(self._root)[0]

  def expand_node(self, node):
    # returns the next possible states that are traversible form one specific
    # node.
    return []

  def set_root(self, new_root):
    self._tree[self._root].append(new_root)
    self._root = new_root
    if new_root not in self._tree:
      self._tree[new_root] = []

  def eval_edge(self, edge):
    # evaluates a single edge - default assumes uniform evaluation of edges.
    return 1
  
  def eval_node(self, node):
    # evaluates a single node - default assumes uniform evaluation of nodes.
    # a node represents a single state
    return 1