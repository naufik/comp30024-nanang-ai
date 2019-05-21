import math
import time
from queue import PriorityQueue
import heapq as heap
from nanang_greedy.game.board import Board
from nanang_greedy.game.move import Move
from nanang_greedy.agent.strategies.minimax import Minimax3Tree
from nanang_greedy.agent.learning import Learner
from nanang_greedy.agent.strategies.mcstree import MonteCarloSearchTree, MonteCarloNode
from nanang_greedy.agent.searchtree import SearchTree
import nanang_greedy.agent.strategies.evals as evals
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
    LEARN = False

    @staticmethod
    def read_weights(color):
        csv_file = open("weights1.csv")
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

    def __init__(self, colour):
        assert(colour in {"red", "green", "blue"})
        self._colour = colour[0].upper()
        self._board = Board(Board.initialize_board())
        self._n_pieces = len(self._board.pieces_of(self._colour))
        # Do extra initialization steps if it is a single_player game/
        self._goals = Player.GOALS[self._colour]
        self._weights = Player.read_weights(self._colour)
        self._eval_func = lambda color, node: evals.eval_one(color, node, weights=self._weights)
        # using a simple Minimax3Tree, replace None with the heuristic function.
        self._search_tree = Minimax3Tree(self._board, self._colour, 1, self._eval_func)
        # self._search_tree = MonteCarloSearchTree(self._board, self._colour,
            # 50)
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
                #check if the next possible move is a weight update
                next_board = self._board.possible_board(move)
                endgame = self._learner.endgame(next_board, self._colour, self._current_state, self._past_boards)
                if endgame == 1:
                    self._states[self._current_state] = endgame
                    self._features[self._current_state] = self._eval_func(self._colour, next_board)[1]
                    self._learner.update_weights(self._states, self._current_state, self._features, self._colour)
                else:
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
            if self._board not in self._past_boards.keys():
                self._past_boards[self._board] = 1
            else:
                self._past_boards[self._board] += 1

            #check if endgame, update weight for losers and draws
            endgame = self._learner.endgame(self._board, self._colour, self._current_state, self._past_boards)
            if endgame == -1 or endgame == 0:
                self._states[self._current_state-1] = endgame
                self._learner.update_weights(self._states, self._current_state, self._features, self._colour)
        self._search_tree.set_root(self._board)
