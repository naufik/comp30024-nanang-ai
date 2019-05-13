import math
import time
from queue import PriorityQueue
import heapq as heap
from nanang.game.board import Board
from nanang.game.move import Move
from nanang.agent.strategies.minimax import Minimax3Tree
from nanang.agent.searchtree import SearchTree
import nanang.agent.strategies.evals as evals
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

    NUM_PIECES_TO_WIN = 4

    @staticmethod
    def update_weights(states, current_state, features):
        print("cool", states)
        print("len states", len(states))
        print("current states", current_state)
        print("features", features)
        print("len features", len(features))
        weights = evals.w
        new_weights = []
        eta = 0.1
        lambDUH = 0.7
        for weight in weights:
            w = weight
            adjustment = 0
            for i in range(current_state):
                # TODO: find gradient
                gradient = features[i][weights.index(w)]
                telescope = 0
                for m in range(i):
                    exponent = m - i
                    dm = states[m]
                    telescope += (lambDUH ** exponent) * dm
                print("telescope ", telescope)
                adjustment += gradient * telescope
            print("adjustment:", adjustment)
            w += eta * adjustment
            new_weights.append(w)
        print("just a test bro", new_weights)
        Player.write_weights(new_weights)

    @staticmethod
    def write_weights(new_weights):
        #TODO: write to txt rather than print lul
        with open('weights.txt', 'w') as f:
            for weight in new_weights:
                f.write(str(weight))
            f.close()

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
        self._features = {}
        self._current_state = 0

    def action(self):
        move, eval_value = self._search_tree.next_best()
        #returns the reward of the state
        if move:
            #check if it is endgame state
            next_board = self._board.possible_board(move)
            endgame = self.endgame(next_board)
            print("endgame value", endgame)
            if endgame is not None:
                print("it's None fam")
                self._states[self._current_state] = endgame
                self._features[self._current_state] = self._eval_func(self._colour, next_board)[1]
                #do I need to do this part if it's being called from update anyways?
                Player.update_weights(self._states, self._current_state, self._features)
            else:
                self._states[self._current_state] = math.atan(eval_value) / math.pi
                self._features[self._current_state] = self._eval_func(self._colour, next_board)[1]
                self._current_state += 1
            return move.to_tuple()
        else:
            return ("PASS", None)


    def update(self, colour, action):
        #print("mercusuar", self._states, self._features, self._current_state)
        move = Move.from_tuple(colour, action)
        self._board = self._board.possible_board(move)
        endgame = self.endgame(self._board)
        print("endgame value central junction bby", endgame)
        if endgame is not None:
            self._states[self._current_state-1] = endgame
            Player.update_weights(self._states, self._current_state, self._features)
        self._search_tree.set_root(self._board)


    def endgame(self, board):
        """
        Checks if the state is an endgame state (win/loss/draw)
        :return: int indicating win/loss/draw with values ranging from [1,-1,0]
        respectively
        """
        #check if player has won the game
        print("kambing")
        print()
        if board._win_state[self._colour] == Player.NUM_PIECES_TO_WIN:
            print("kontol")
            return Player.ENDGAME_STATES["WIN"]
        #check if enemy has won the game
        others = {"R", "G", "B"} - {self._colour}
        for colour in others:
            if board._win_state[colour] == Player.NUM_PIECES_TO_WIN:
                print("ngehe")
                return Player.ENDGAME_STATES["LOSS"]
        #TODO: check for draws
        return None
