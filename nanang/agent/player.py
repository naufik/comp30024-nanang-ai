import math
import time
from queue import PriorityQueue
import heapq as heap
from nanang.game.board import Board
from nanang.game.move import Move

from nanang.agent.strategies.minimax import Minimax3Tree
from nanang.agent.searchtree import SearchTree
from random import Random

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
        self._colour = colour[0].upper()
        self._board = Board(Board.initialize_board())
        self._n_pieces = len(self._board.pieces_of(self._colour))

        # Do extra initialization steps if it is a single_player game/
        self._goals = Player.GOALS[self._colour]

        # using a simple Minimax3Tree, replace None with the heuristic function.
        self._search_tree = Minimax3Tree(self._board, self._colour, 1, 
            lambda c, x: self.board_evaluation(c, x))

    def board_evaluation(self, colour, board: Board):
        """

        :param colour:
        :param board:
        :return:
        """

        enemy_dist = 0
        player_pieces = len(board.pieces_of(self._colour))

        # calculate distance for enemy players to their goal
        player_dist = 0
        enemy_pieces = 0
        for player, goals in Player.GOALS.items():
            pieces = board.pieces_of(player)
            for piece_coor in pieces:
                if player == self._colour:
                    player_dist += Player.dist_nearest_goal(piece_coor, goals)
                else:
                    enemy_dist += Player.dist_nearest_goal(piece_coor, goals)
            if player != self._colour:
                enemy_pieces += len(board.pieces_of(player))

        ngasal = 0.5
        lebih_ngasal = 1.1
        return -lebih_ngasal*player_dist + ngasal*enemy_dist + lebih_ngasal*player_pieces - ngasal*enemy_pieces

    @staticmethod
    def dist_nearest_goal(piece, goals):
        minimum = 0
        flag = True
        for goal in goals:
            dist = Player._dist(piece, goal)
            if flag:
                minimum = dist
                flag = False
            elif dist < minimum:
                minimum = dist
        return minimum

    @staticmethod
    def _dist(x, y):
        return max(x[0] - y[0], x[1] - y[1], (-x[0] - x[1]) - (-y[0] - y[1]))

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
        move: Move = self._search_tree.next_best()
        if move:
            return move.to_tuple()
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
            self._board = self._board.possible_board(move)
            self._search_tree.set_root(self._board)
  
    def is_goal(self, current):
        """
        Checks if the state passed in current is a goal state.
        """
        return (len(current.pieces_of(self._colour)) == 0)