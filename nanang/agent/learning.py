import csv

class Learner:

    ENDGAME_STATES = {"WIN": 1, "LOSS": -1, "DRAW": 0}
    NUM_PIECES_TO_WIN = 4
    MAX_STATES = 254

    def __init__(self, weights):
        self._weights = weights

    def update_weights(self, state_evals, current_state, features, colour):
        """
        Calculates new weights based on the TD-Leaf Lambda formula
        :param state_evals: The reward value for all states for this particular game
        :param current_state: The total number of states within this particular game
        :param features: The feature values for all states for this paricular game
        :param colour: The player for which this weight update calculation is relevant to
        """

        weights = self._weights
        new_weights = []
        eta = 0.1
        lambDUH = 0.7
        new_weights.append(colour)
        for weight in weights:
            w = weight
            adjustment = 0
            for i in range(current_state-1):
                # TODO: find gradient
                gradient = features[i][weights.index(w)]
                telescope = 0
                for m in range(i, current_state-1):
                    exponent = m - i
                    dm = state_evals[m+1] - state_evals[m]
                    telescope += (lambDUH ** exponent) * dm
                adjustment += gradient * telescope
            w += eta * adjustment
            new_weights.append(str(w))
        print("New Weight: ", new_weights)
        Learner.write_weights(new_weights)

    def endgame(self, board, colour, current_state, past_boards):
        """
        Checks if the state is an endgame state (win/loss/draw)
        :return: Integer indicating win/loss/draw with values ranging from [1,-1,0] respectively
        """
        #check if player has won the game
        if board._win_state[colour] == Learner.NUM_PIECES_TO_WIN:
            return Learner.ENDGAME_STATES["WIN"]
        #check if enemy has won the game
        others = {"R", "G", "B"} - {colour}
        for colour in others:
            if board._win_state[colour] == Learner.NUM_PIECES_TO_WIN:
                return Learner.ENDGAME_STATES["LOSS"]
        #check for draws
        if current_state == Learner.MAX_STATES:
            return Learner.ENDGAME_STATES["DRAW"]
        for occurrences in past_boards.values():
            if occurrences == 4:
                return Learner.ENDGAME_STATES["DRAW"]
        return None


    @staticmethod
    def write_weights(new_weights):
        with open('weights.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(new_weights)
            csvFile.close()