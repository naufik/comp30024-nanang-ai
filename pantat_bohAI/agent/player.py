import math
import time
from queue import PriorityQueue
import heapq as heap
from pantat_bohAI.game.board import Board
from pantat_bohAI.game.move import Move
from pantat_bohAI.agent.strategies.minimax import Minimax3Tree
from pantat_bohAI.agent.learning import Learner
from pantat_bohAI.agent.strategies.mcstree import MonteCarloSearchTree, MonteCarloNode
from pantat_bohAI.agent.searchtree import SearchTree
from random import SystemRandom
import pantat_bohAI.agent.strategies.evals as evals
import csv
import cProfile


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

    #enable and disable learning
    LEARN = True

    @staticmethod
    def read_weights(color):
        try:
            csv_file = open("weights.csv")
            lines = list(filter(bool, csv.reader(csv_file)))
            lines.reverse()
            lines = sorted(lines[:3])
            if color == "B":
                return list(map(float, lines[0][1:]))
            elif color == "G":
                return list(map(float, lines[1][1:]))
            elif color == "R":
                return list(map(float, lines[2][1:]))
            assert (False)
        except:
            rng = SystemRandom()
            return [rng.randint(-100,100) for i in range(2750)]

    def __init__(self, colour):
        assert(colour in {"red", "green", "blue"})
        self._colour = colour[0].upper()
        self._board = Board(Board.initialize_board())
        self._n_pieces = len(self._board.pieces_of(self._colour))
        
        self._goals = Player.GOALS[self._colour]
        self._weights = Player.read_weights(self._colour)
        self._eval_func = lambda color, node: evals.meta_eval(color, node, self._weights)

        self._search_tree = Minimax3Tree(self._board, self._colour, 4, self._eval_func)
        
        self._states = {}
        self._features = {}
        if Player.LEARN:
            self._current_state = 0
            self._past_boards = {}
            self._past_boards[self._board] = 1
            self._learner = Learner(self._weights)

    def action(self):
        move, eval_value = self._search_tree.next_best()
        #returns the reward of the state
        if move:
            if Player.LEARN:
                #check if the next possible move results the player winnning the game
                next_board = self._board.possible_board(move)
                endgame = self._learner.endgame(next_board, self._colour, self._current_state, self._past_boards)
                if endgame == 1:
                    #store the current state's reward value as the winning endgame utility value, 1
                    self._states[self._current_state] = endgame
                    self._features[self._current_state] = self._eval_func(self._colour, next_board)[1]
                    #update the weights
                    self._learner.update_weights(self._states, self._current_state, self._features, self._colour)
                else:
                    #store reward value as the current state's evaluation value mapped to arctan
                    self._states[self._current_state] = math.atan(eval_value) / math.pi
                    self._features[self._current_state] = self._eval_func(self._colour, next_board)[1]
                    self._current_state += 1
            return move.to_tuple()
        else:
            return ("PASS", None)


    def update(self, colour, action):
        #update existing board
        move = Move.from_tuple(colour, action)
        self._board = self._board.possible_board(move)
        if Player.LEARN:
            #track the number of times a particular state for a board has occured
            if self._board not in self._past_boards.keys():
                self._past_boards[self._board] = 1
            else:
                self._past_boards[self._board] += 1

            #check if the current state is an endgame state, that being a draw (0) or a loss (-1)
            endgame = self._learner.endgame(self._board, self._colour, self._current_state, self._past_boards)
            if endgame == -1 or endgame == 0:
                self._states[self._current_state-1] = endgame
                #update the weights
                self._learner.update_weights(self._states, self._current_state, self._features, self._colour)
        self._search_tree.set_root(self._board)
