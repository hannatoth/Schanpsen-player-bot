"""
ADAPT U Bot -- Chooses a move that adapts to the current risk state of the
game, using SMT-based logical reasoning (Z3).
"""

# Import the API objects
from api import State, Deck, util
# Import the Z3 solver objects
from z3 import *

class Bot:

    ######## INITIALIZER ############
    def __init__(self):
        pass

    ####### GET MOVE #############
    def get_move(self, state):
        moves = state.moves()
        high_adpt = self.models_highadpt()
        mid_adpt = self.models_midadpt()
        low_adpt = self.models_lowadpt()
        risk_state = self.determine_riskstate(state)


        if risk_state == "high risk":
            print("High risk state detected, adapting strategy")
            for move in moves:
                adpt_model = self.create_adptmodel(move, state)
                if adpt_model is None:
                    adpt_model = []
                for x in high_adpt:
                    list_comparison = []
                    for feature in x:
                        if feature in adpt_model:
                            list_comparison.append(feature)
                    if len(list_comparison) == len(adpt_model):
                        return move
            for move in moves:
                adpt_model = self.create_adptmodel(move, state)
                if adpt_model is None:
                    adpt_model = []
                for x in mid_adpt:
                    list_comparison = []
                    for feature in x:
                        if feature in adpt_model:
                            list_comparison.append(feature)
                    if len(list_comparison) == len(adpt_model):
                        return move
            for move in moves:
                adpt_model = self.create_adptmodel(move, state)
                if adpt_model is None:
                    adpt_model = []
                for x in low_adpt:
                    list_comparison = []
                    for feature in x:
                         if feature in adpt_model:
                            list_comparison.append(feature)
                    if len(list_comparison) == len(adpt_model):
                        return move

        if risk_state == "mid risk":
            print("Medium risk state detected, adapting strategy")
            for move in moves:
                adpt_model = self.create_adptmodel(move, state)
                if adpt_model is None:
                    adpt_model = []
                for x in mid_adpt:
                    list_comparison = []
                    for feature in x:
                        if feature in adpt_model:
                            list_comparison.append(feature)
                    if len(list_comparison) == len(adpt_model):
                        return move
            for move in moves:
                adpt_model = self.create_adptmodel(move, state)
                if adpt_model is None:
                    adpt_model = []
                for x in low_adpt:
                    list_comparison = []
                    for feature in x:
                        if feature in adpt_model:
                            list_comparison.append(feature)
                    if len(list_comparison) == len(adpt_model):
                        return move

        if risk_state == "low risk":
            print("Low risk state detected.")
            for move in moves:
                adpt_model = self.create_adptmodel(move, state)
                if adpt_model is None:
                    adpt_model = []
                for x in low_adpt:
                    list_comparison = []
                    for feature in x:
                        if feature in adpt_model:
                            list_comparison.append(feature)
                    if len(list_comparison) == len(adpt_model):
                        return move

        return self.lowest_value(moves)

    def models_highadpt(self):
        ###### Modelling all high risk states ################
        p1_trumps = Int('p1_trumps')
        defeat_rank = Int('defeat_rank')
        prob_higher = Int("prob_higher")
        def_higher = Int("def_higher")
        high_stakes = Int('high_stakes')
        adaptation_score = Int("adaptation_score")

        s = Solver()
        s.add(adaptation_score == p1_trumps + defeat_rank + prob_higher + def_higher + high_stakes)
        s.add(Or(high_stakes == 2, high_stakes == 0))
        s.add(Or(p1_trumps == 3, p1_trumps == 0))
        s.add(Or(defeat_rank == 2, defeat_rank == 0))
        s.add(0 <= prob_higher)
        s.add(prob_higher <= 2)
        s.add(Or(def_higher == 2, def_higher == 0))
        s.add(adaptation_score >= 5)
        s.add(adaptation_score <= 10)

        model_list = []
        while s.check() == z3.sat:
            solution = "False"
            m = s.model()
            model_list.append(m)
            for i in m:
                solution = f"Or(({i} != {m[i]}), {solution})"
            f2 = eval(solution)
            s.add(f2)

        model_list2 = []
        for i in model_list:
            i = str(i)
            model_list2.append(i)

        high_adaptation_models = []
        for j in model_list2:
            string1 = ''.join(j)
            string1 = string1[1:]
            string1 = string1[:-1]
            string1 = string1.split(", ")
            high_adaptation_models.append(string1)

        return high_adaptation_models

    def models_midadpt(self):
        ###### Modelling all mid risk states ################
        p1_trumps = Int('p1_trumps')
        defeat_rank = Int('defeat_rank')
        prob_higher = Int("prob_higher")
        def_higher = Int("def_higher")
        high_stakes = Int('high_stakes')
        adaptation_score = Int("adaptation_score")

        s = Solver()
        s.add(adaptation_score == p1_trumps + defeat_rank + prob_higher + def_higher + high_stakes)
        s.add(Or(high_stakes == 2, high_stakes == 0))
        s.add(Or(p1_trumps == 3, p1_trumps == 0))
        s.add(Or(defeat_rank == 2, defeat_rank == 0))
        s.add(0 <= prob_higher)
        s.add(prob_higher <= 2)
        s.add(Or(def_higher == 2, def_higher == 0))
        s.add(adaptation_score >= 2)
        s.add(adaptation_score <= 4)

        model_list = []
        while s.check() == z3.sat:
            solution = "False"
            m = s.model()
            model_list.append(m)
            for i in m:
                solution = f"Or(({i} != {m[i]}), {solution})"
            f2 = eval(solution)
            s.add(f2)

        model_list2 = []
        for i in model_list:
            i = str(i)
            model_list2.append(i)

        mid_adaptation_models = []
        for j in model_list2:
            string1 = ''.join(j)
            string1 = string1[1:]
            string1 = string1[:-1]
            string1 = string1.split(", ")
            mid_adaptation_models.append(string1)

        return mid_adaptation_models

    def models_lowadpt(self):
        ###### Modelling all mid risk states ################
        p1_trumps = Int('p1_trumps')
        defeat_rank = Int('defeat_rank')
        prob_higher = Int("prob_higher")
        def_higher = Int("def_higher")
        high_stakes = Int('high_stakes')
        adaptation_score = Int("adaptation_score")

        s = Solver()
        s.add(adaptation_score == p1_trumps + defeat_rank + prob_higher + def_higher + high_stakes)
        s.add(Or(high_stakes == 2, high_stakes == 0))
        s.add(Or(p1_trumps == 3, p1_trumps == 0))
        s.add(Or(defeat_rank == 2, defeat_rank == 0))
        s.add(0 <= prob_higher)
        s.add(prob_higher <= 2)
        s.add(Or(def_higher == 2, def_higher == 0))
        s.add(adaptation_score >= 0)
        s.add(adaptation_score <= 1)

        model_list = []
        while s.check() == z3.sat:
            solution = "False"
            m = s.model()
            model_list.append(m)
            for i in m:
                solution = f"Or(({i} != {m[i]}), {solution})"
            f2 = eval(solution)
            s.add(f2)

        model_list2 = []
        for i in model_list:
            i = str(i)
            model_list2.append(i)

        low_adaptation_models = []
        for j in model_list2:
            string1 = ''.join(j)
            string1 = string1[1:]
            string1 = string1[:-1]
            string1 = string1.split(", ")
            low_adaptation_models.append(string1)

        return low_adaptation_models

    def lowest_value(self, moves):
        lowest_val = moves[0]
        for move in moves:
            if lowest_val[0] is not None and move[0] is not None and lowest_val[0] % 5 <= move[0] % 5:
                lowest_val = move
        return lowest_val

    def determine_riskstate(self, state):
        risk_score = util.ratio_points(state, 1) * 2.0 - 1.0
        if risk_score <= 0:
            risk_state = "high risk"
            return risk_state
        elif risk_score >= 0.5:
            risk_state = "low risk"
            return risk_state
        else:
            risk_state = "mid risk"
            return risk_state

    def create_adptmodel(self, move, state):
        adpt_model = []
        adaptation_score = 0
        if move[0] is not None and util.get_suit(move[0]) == state.get_trump_suit():
            adpt_model.append('p1_trumps = 3')
            adaptation_score += 3
        if move[0] is None or util.get_suit(move[0]) != state.get_trump_suit():
            adpt_model.append('p1_trumps = 0')
        opp_card = state.get_opponents_played_card()
        if state.leader() == 2:
            if move[0] is not None and opp_card is not None and util.get_suit(move[0]) == util.get_suit(opp_card) and move[0] % 5 <= opp_card % 5:
                adpt_model.append('defeat_rank = 2')
                adaptation_score += 2
            if move[0] is None or opp_card is None or util.get_suit(move[0]) != util.get_suit(opp_card) or move[0] % 5 > opp_card % 5:
                adpt_model.append('defeat_rank = 0')
        if state.leader() == 2:
            adpt_model.append('high_stakes = 0')
        if state.leader() == 1:
            adpt_model.append('defeat_rank = 0')
        if state.leader() == 1:
            if move[0] is not None and move[0] % 5 <= 1:
                adpt_model.append('high_stakes = 2')
                adaptation_score += 2
            else:
                adpt_model.append('high_stakes = 0')
        if state.get_phase() == 1:
            perspective = state.get_perspective()
            unknowns = []
            for index, card in enumerate(perspective):
                search_term = 'U'
                if card == search_term:
                    unknowns.append(index)
            u = len(unknowns)
            problematicCards = []
            for unknown in unknowns:
                if (move[0] is not None and (Deck.get_suit(unknown) == Deck.get_suit(move[0])) and unknown < move[0]):
                    problematicCards.append(unknown)
            pc = len(problematicCards)
            probability = (u - pc) / u
            if probability >= 0.8:
                adpt_model.append('prob_higher = 2')
                adaptation_score += 2
            elif probability >= 0.4 and probability < 0.8:
                adpt_model.append('prob_higher = 1')
                adaptation_score += 1
            else:
                adpt_model.append('prob_higher = 0')
                adaptation_score += 0
            if state.get_phase() == 2:
                adpt_model.append('prob_higher = 0')
            opp_hand = []
            perspective = state.get_perspective()
            for index, card in enumerate(perspective):
                search_term = 'P2H'
                if card == search_term:
                    opp_hand.append(index)
            if len(opp_hand) > 0:
                for card in opp_hand:
                    if move[0] is not None and util.get_suit(card) == util.get_suit(move[0]) and move[0] % 5 < card % 5:
                        adpt_model.append('def_higher = 2')
                        adaptation_score += 2
                    else:
                        adpt_model.append('def_higher = 0')
            if state.get_phase() == 1:
                adpt_model.append('def_higher = 0')
            adpt_model.append('adaptation_score = {}'.format(adaptation_score))
            return adpt_model
