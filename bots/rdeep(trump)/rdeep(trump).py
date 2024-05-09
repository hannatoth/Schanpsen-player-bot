# Import the API objects
from api import State, util, Deck
import random


class Bot:
    # How many samples to take per move
    __num_samples = -1
    # How deep to sample
    __depth = -1

    def __init__(self, num_samples=4, depth=8):
        self.__num_samples = num_samples
        self.__depth = depth

    def get_move(self, state):

        # See if we're player 1 or 2
        player = state.whose_turn()

        # Get a list of all legal moves
        moves = state.moves()

        # Sometimes many moves have the same, highest score, and we'd like the bot to pick a random one.
        # Shuffling the list of moves ensures that.
        random.shuffle(moves)

        best_score = float("-inf")
        best_move = None

        scores = [0.0] * len(moves)

        for move in moves:
            for s in range(self.__num_samples):

                # If we are in an imperfect information state, make an assumption.

                sample_state = state.make_assumption() if state.get_phase() == 1 else state

                score = self.evaluate(sample_state.next(move), player)

                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move  # Return the best scoring move

    def evaluate(self,
                 state,  # type: State
                 player  # type: int
                 ):
        # type () -> float

        score = 0.0

        for _ in range(self.__num_samples):

            st = state.clone()

            # Do some random moves
            for i in range(self.__depth):
                if st.finished():
                    break

                st = st.next(random.choice(st.moves()))

            score += self.heuristic(st, player)

        return score / float(self.__num_samples)

    def heuristic(self, state, player):
        moves = state.moves()
        # print(moves)

        howmany_trumps = 0
        score = 0
        matrixrange = range(15, 20)

        if Deck.get_trump_suit == "S":
            matrixrange = (15, 20)
        elif Deck.get_trump_suit == "H":
            matrixrange = (10, 15)
        elif Deck.get_trump_suit == "D":
            matrixrange = (5, 10)
        elif Deck.get_trump_suit == "C":
            matrixrange = (0, 5)

        lst_of_move_numbers = []
        for _tuple in moves:
            if type(_tuple[0]) != type(None) and type(_tuple[1]) == type(None):
                lst_of_move_numbers.append(_tuple[0])
        #print(lst_of_move_numbers)
        for move_number in lst_of_move_numbers:
            score = 3 - ((move_number % 5) - 2)
            if move_number in matrixrange:
                howmany_trumps += 1
        score += 5 * howmany_trumps
        # print(score)
        return score
