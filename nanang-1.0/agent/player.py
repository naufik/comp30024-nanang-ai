import math
from queue import PriorityQueue
import heapq as heap

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
    
    @staticmethod
    def _cost(move):
        #uniform move cost of 1 for all possible moves that can be made in the board
        return 1

    @staticmethod
    def _dist(x, y):
        """
        calculates euclidian distance between two points
        :param x: first coordinate
        :param y: second coordinate
        :return: hex manhattan distance

        formula taken from https://www.redblobgames.com/grids/hexagons/#distances
        """
        
        return max(x[0]-y[0], x[1]-y[1], (-x[0]-x[1])-(-y[0]-y[1]))

    def __init__(self, board, color, single=True):
        assert(board is not None and color in {"R", "G", "B"})
        self.start = board
        self.color = color
        self.n_pieces = len(board.pieces_of(color))
        
        # Do extra initialization steps if it is a single_player game/
        if single:
            self._goals = list(filter(lambda x: board._dict_rep[x] != 'X',
                Player.GOALS[self.color]))

    #pseudo-code for A*, define methods inside board
    def find_path(self):
        """
        Attempts to find a path from the state stored in current.start, to any
        possible goal states.

        original A* sourcecode: https://www.redblobgames.com/pathfinding/a-star/introduction.html
        :return: an array of the moves needed for all tiles to exit the board
        """

        frontier = [(0, self.start)]
        came_from = dict()
        came_from[self.start] = None
        cost_so_far = dict()
        cost_so_far[self.start] = 0

        while len(frontier) > 0:
            #explore the state that has a the highest priority
            current = heap.heappop(frontier)[1]

            #checks if the state is the goal state
            if self.is_goal(current):
                break

            #explores all possible moves that can be made from the current board state
            for next_move in current.possible_moves(self.color):

                #calculate the cost so far after the next possible move
                new_cost = cost_so_far[current] + Player._cost(next_move)
                next_board = current.possible_board(next_move)

                #evaluate board state
                if next_board not in cost_so_far or new_cost < cost_so_far[next_board]:
                    cost_so_far[next_board] = new_cost
                    priority = new_cost + self.evaluate_board(next_board)
                    heap.heappush(frontier, (priority, next_board))
                    came_from[next_board] = (next_move, current)

        return self.construct_path(came_from, current)
    
    def is_goal(self, current):
        """
        Checks if the state passed in current is a goal state.
        """
        return (len(current.pieces_of(self.color)) == 0)

    def construct_path(self, came_from, came_to):
        """
        A helper method to construct a path from the starting point to the
        goal state that has already been found.
        """
        mv, current = (None, came_to)
        path = []
        moves = []

        #trace back through the dictionary and recreate the path
        while current != self.start:
            path.append(current)
            if mv is not None:
                moves.append(mv)
            mv, current = came_from[current]

        path.reverse()
        moves.append(mv)
        moves.reverse()
        return moves
    
    def evaluate_board(self, board):
        """
        Evaluates the heuristic score of a new board (not the starting board). 
        See the report for details about the evaluation function being
        implemented here.

        This evaluation function is to be used with the A* pathfinding.

        :param pieces: array of the coordinates of pieces on the board
        :param goals: array of the coordinates of goals (relevant to piece(s)) on the board
        :return: sum of minimum distances
        """

        pieces = board.pieces_of(self.color)
        goals = self._goals

        #probability of finding another piece on the board
        prob_factor = (len(pieces) - 1) / 37

        #find the total sum of minimum distance(s) for the piece(s) to their goal tile(s)
        totalMinimum = 0
        for key in pieces:
            minimum = 0
            flag = True
            for goal in goals:
              heur = (4/7 * prob_factor + (1-prob_factor)) * (Player._dist(key, goal) + 1)
              if flag:
                minimum = heur
                flag = False
              elif heur<minimum:
                minimum = heur
            totalMinimum+=minimum

        return totalMinimum