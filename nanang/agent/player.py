import math
from queue import PriorityQueue
import heapq as heap
from game.board import Board
from game.move import Move

from agent.strategies.minimax import Minimax3Tree
from agent.searchtree import SearchTree

class Player:
    """
    Use boards and states,
    moves as nodes,
    """

    GOALS = {        
        "R": [(3, -3), (3, -2), (3, -1), (3, 0)],
        "G":  [(-3, 3), (-2, 3), (-1, 3), (0, 3)],
        "B":  [(0, -3), (-1, -2), (-2, -1), (-3, 0)]
    }


    # def __init__(self, board, color, single=True):
    def __init__(self, colour):
        assert(colour in {"red", "green", "blue"})
        self.colour = colour[0].upper()
        self.board = Board(Board.initialize_board())
        self.n_pieces = len(self.board.pieces_of(colour))

        # Do extra initialization steps if it is a single_player game/
        self._goals = Player.GOALS[self.colour]

        # using a simple Minimax3Tree, replace None with the heuristic function.
        self._search_tree = Minimax3Tree(self.board, self.colour, 1, None)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed
        actions, your player must return a pass instead. The action (or pass)
        must be represented based on the above instructions for representing
        actions.
        """
        # TODO: Decide what action to take.

        # selangkah_keseberang = True
        # if selangkah_keseberang:
        #     return move.to_tuple()
        move = self._search_tree.next_best().to_tuple()
        if move:
            return move
        else:
            return ("PASS", None)

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red",
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action
        (or pass) for the player colour (your method does not need to validate
        the action/pass against the game rules).
        """
        if (action[0] != "PASS"):
            move = Move.from_tuple(colour, action)
            self.board = self.board.possible_board(move)
            self._search_tree.set_root(self.board)
  
    def is_goal(self, current):
        """
        Checks if the state passed in current is a goal state.
        """
        return (len(current.pieces_of(self.colour)) == 0)