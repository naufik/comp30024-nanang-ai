from nanang.agent.searchtree import SearchTree

class RegTree(SearchTree):
  """
  A type of Learned Tree based on linear regression
  """

  def __init__(self, root, weights_file):
    super().__init__(root)