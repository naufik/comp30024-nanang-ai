import math
import time
from queue import PriorityQueue
import heapq as heap
from nanang.game.board import Board
from nanang.game.move import Move
from nanang.agent.strategies.minimax import Minimax3Tree
from nanang.agent.searchtree import SearchTree
import nanang.agent.strategies.evals as evals
import numpy as np
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

    ENDGAME_STATES = {"WIN": 1, "LOSS": -1, "DRAW": 0}

    @staticmethod
    def update_weights(states, current_state, features):
        weights = evals.w
        new_weights = []
        eta = 0.1
        lambDUH = 0.7
        for weight in weights:
            w = weight
            adjustment = 0
            for i in range(current_state):
                # TODO: find gradient
                gradient = features[i]
                telescope = 0
                for m in range(i):
                    exponent = m - i
                    dm = states[m]
                    telescope += (lambDUH ** exponent) * dm
                adjustment += gradient * telescope
            w += eta * adjustment
            new_weights.append(w)
        Player.write_weights(new_weights)

    @staticmethod
    def write_weights(new_weights):
        #TODO: write to txt rather than print lul
        with open('weights.txt', 'w') as f:
            for weight in new_weights:
                f.write("%s\n" % weight)

    def __init__(self, colour):
        assert(colour in {"red", "green", "blue"})
        self._colour = colour[0].upper()
        self._board = Board(Board.initialize_board())
        self._n_pieces = len(self._board.pieces_of(self._colour))
        # Do extra initialization steps if it is a single_player game/
        self._goals = Player.GOALS[self._colour]
        self._eval_func = evals.eval_one
        # using a simple Minimax3Tree, replace None with the heuristic function.
        self._search_tree = Minimax3Tree(self._board, self._colour, 1, self._eval_func)
        self._states = {}
        self._current_state = 1

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

        move, eval_value = self._search_tree.next_best()
        #returns the reward of the state
        if move:
            #check if it is endgame state
            endgame = self.endgame()
            if endgame is not None:
                self._states[self._current_state] = endgame
                next_board = self._board.possible_board(move)
                features = self._eval_func(self._colour, next_board)[1]
                Player.update_weights(self._states, self._current_state, features)
            else:
                self._states[self._current_state] = np.arctan(eval_value) / np.pi
                self._current_state += 1

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
        move = Move.from_tuple(colour, action)
        self._board = self._board.possible_board(move)
        endgame = self.endgame()
        if endgame is not None:
            self._states[self._current_state] = endgame
            Player.update_weights(self._states, self._current_state)
        self._search_tree.set_root(self._board)
  
    def is_goal(self, current):
        """
        Checks if the state passed in current is a goal state.
        """
        return (len(current.pieces_of(self._colour)) == 0)

    def endgame(self):
        """
        Checks if the state is an endgame state (win/loss/draw)
        :return: int indicating win/loss/draw with values ranging from [1,-1,0]
        respectively
        """
        all_exit = 0
        #check if player has won the game
        if self._board._win_state[self._colour] == all_exit:
            return Player.ENDGAME_STATES["WIN"]
        #check if enemy has won the game
        others = {"R", "G", "B"} - {self._colour}
        for colour in others:
            if self._board._win_state[colour] == all_exit:
                return Player.ENDGAME_STATES["LOSS"]
        #TODO: check for draws
        return None
