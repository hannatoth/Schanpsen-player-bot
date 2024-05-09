import state
from api import State, util, Deck
import random


def sortWithremainder(lst_of_moves):
    v = [[] for i in range(5)]
    for i in range(len(lst_of_moves)):
        if type(lst_of_moves[i]) != type(None):
            v[lst_of_moves[i] % 5].append(lst_of_moves[i])
    for i in range(5):
        v[i].sort()
    index_of_goal_lst = 0
    for i in range(5):
        for members_of_inner_lst in v[i]:
            lst_of_moves[index_of_goal_lst] = members_of_inner_lst
            index_of_goal_lst += 1
    return lst_of_moves


def move_sorter(lst_of_moves):
    if Deck.get_trump_suit(Deck) == "H":
        trump_range = [i for i in range(10, 15)]
    elif Deck.get_trump_suit(Deck) == "D":
        trump_range = [i for i in range(5, 10)]
    elif Deck.get_trump_suit(Deck) == "S":
        trump_range = [i for i in range(15, 20)]
    else:
        trump_range = [i for i in range(0, 5)]

    trumps_in_hand = []
    for i in range(len(lst_of_moves)):
        if lst_of_moves[i] in trump_range:
            trumps_in_hand.append(lst_of_moves[i])
            lst_of_moves.remove(lst_of_moves[i])
    sortWithremainder(lst_of_moves)
    sortWithremainder(trumps_in_hand)
    bestest_moves = lst_of_moves[::-1]
    for i in range(len(trumps_in_hand)):
        bestest_moves.append(trumps_in_hand[i])
    if State.get_phase(State) == 1:
        best_move = bestest_moves[0]
    else:
        best_move = bestest_moves[-1]
    move_tuple = (best_move, None)
    return move_tuple


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
        best_moves = []
        best_moves2 = []
        scores = [0.0] * len(moves)

        for move in moves:
            for s in range(self.__num_samples):

                # If we are in an imperfect information state, make an assumption.

                sample_state = state.make_assumption() if state.get_phase() == 1 else state

                score = self.evaluate(sample_state.next(move), player)
                best_moves.append(move[0])
                # print(len(best_moves))
                for i in best_moves:
                    if i == max(best_moves):
                        best_moves2.append(i)

                return move_sorter(best_moves2)

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
        return util.ratio_points(state, player)
