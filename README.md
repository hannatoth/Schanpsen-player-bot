# Schanpsen-player-bot

# The Effect of Sample Size and Heuristics on the Performance of PIMCS


## Abstract

The well-known Central-European card game Schnapsen, involving two opponent players and 20 cards, can be split into 2 phases. The first phase’s complexity reaches far beyond simple bottom-up algorithms, since most of the cards remain unknown to the agents. An efficient player, therefore, must aim for a strategy that emulates the success rates of perfect-information decisions. The main approach is to roughly estimate the strength of each game-state, despite lacking the majority of the necessary information, purely based on partial knowledge, heuristics, and probabilities.

Our paper aims to identify the determinant factor of the efficacy of Perfect Information Monte Carlo Sampling, used by a Schnapsen playing bot: an enlarged sample size or the fine-tuned heuristics implemented to the bot’s code. The results show that heuristics play a significantly bigger role in a bot’s performance, compared to changes in sample size.

## Research question

Every human or agent has to deal with imperfect information to some degree. In Schnapsen the calculation of every possibility would round up to a computationally infeasible amount of data.

One common way of dealing with imperfect information has been to avoid the issue. Instead of solving a full game, perfect information worlds from the game are sampled and solved either exactly or heuristically. This approach, also called Perfect Information Monte Carlo Sampling (PIMCS), has produced expert-caliber players in games like Skat and Bridge.

We were, therefore, curious about the key element of PIMSC strategy, and how can it be further improved. The paper concludes the experiments, using a bot, Rdeep, and aims to answer the following research question:

**How does the success rate of a PIMSC based player change with modifying search depth and sampling size compared to implementing heuristics in the case of playing Schnapsen?**

## Background


### Schnapsen

Schnapsen is a two-player trick-taking card game originating from the Habsburg Monarchy, and has the aim to collect 66 points through capturing the opponent’s cards. The set of cards are a plucked version of the standard international playing cards, removing cards from two to nine. Ranking and points are not straightforward, Jacks, Queens, Kings, Tens, and Aces are worth 2, 3, 4, 10, and 11 points respectively.

The game has two phases: first both players get a hand of five cards. A trump card is then revealed on the desk, deciding the trump suit. The first player plays a card, hoping the opponent has no trump cards, and no card that follows suit having a higher value, as these are the only ways one wins a round.

The game enters the second phase once the talon is exhausted, meaning every known card is either already played or is in the player’s own hands, leaving only five possible cards in the opponent’s hand. In such a case it is only a matter of evaluating the options, deciding on a winning strategy or surrendering.

This description purposefully lacks some of Schnapsen’s features, such as closing the talon, as this simplification greatly simplifies the game without drastically disturbing game rules.

### Rdeep

The schnapsen bot, Rdeep uses a form of Perfect Information Monte-Carlo sampling.

It chooses a strategy by playing an assumption about the possible combination of unknown cards, to an end state, then evaluating the degree of success of the end state. When evaluating an assumed possible state, Rdeep plays the game to completion, or to the previously set depth, by assuming that each player makes a random choice for every move.

Each randomly guessed state is sampled like this several times to estimate the general success rate, the sequences of moves possibly have. The scores are compared, then a path is chosen randomly out of the sequences that give the best results.

## Future Work

Without doubt, the most important thing to improve upon the work described in this research would be to push the number and quality of the implemented heuristics.

The purpose of ranking the cards by strength, is to create a feature vector for each possible belief state of the game. Based on this vector the agent is able to evaluate how much a move would affect the hand’s potential to gain points in the upcoming states. Considering this could be done in the first turn of the game with as little as 32 belief state samples, this does not seem like an unrealistic goal to achieve. However, it is necessary to see how much value does the specific heuristic has compared to increasing the sampling database.

Costwise, the time-, and-space-complexity of calculating one particular potential move did not significantly increase with either options, so the only measurable factor remains the number of scored points in each game. To gain relevant insight into the efficiency of heuristics, we should create more in-depth variants of state-evaluation. Due to the restricted time, this paper only focuses on the ones that eval- uate future hand-potential. It provides guidelines on what evaluation strate- gies need further exploration, for instance: precise prediction of the opponent possible cards, counting the ratio of strong cards in the players’ hands or the tallon etc. The results forecast that the heuristics should be combined in order to outplay the bots using enlarged sampling size.


## Experimental Setup

The hypothesis was that changing either the sample size or the depth of a bot which relies heavily on PIMS would result in a greater change in the outcome of games, than the implementation of heuristics to the same bot would.
The framework for the experiment is very straight forward. We cre- ated 4 different bots (all based on PIMS): rdeep(trump), rdeep(higher-lower), rdeep(bigsample) and rdeep(bigdepth).
Rdeep(trump) is a bot which evaluates a given position by the number of trumps it has in it’s hands, rather than by the number of points it has accumulated and it uses this information to act accordingly.
Rdeep(higher-lower) is a similar bot, however the main difference is that it evaluates every single card in the sample of possible moves and orders them from best to worst and in the first phase of the game it opts for the weakest possible choice, while it does the opposite in the second phase, where it always plays the strongest possible move.
Rdeep(bigsample) is a PIMS based bot that has a larger than average sample size and from this increased amount of data it has a ”better under- standing” of what move it should play, meaning that it will make a choice based upon more variables.
Rdeep(bigdepth) also has more data to work with, however this data is directed towards going deeper down into the search branches.

## Statistical testing and Conclusion

The way we tested the hypothesis was by running 4 separate tournaments, each of our bots versus a bot which plays random legal moves. Of course we had to keep in mind that the game is a partial information game and there is also a great amount of luck involved with the cards you are dealt. Therefore the amount of games played must be substantial, we went with 5000 parties between pairs.
From the tournaments played we could gather statistics on how many points our bots won against the random bot. This information is of essence because the relative distance from the original ratio of points between the two bots (random bot vs rdeep bot) gives us a numerical value of how significant the changes were with regards to the outcome of the tournament.

The findings clearly disprove our hypothesis. The relative distance from the original ratio of points gained shifted drastically with the implementation of heuristics to the bots, while the tinkering of sample sizes an depths only nudged the ratio a small amount.
Our experiment concludes that the rdeep bot, while using the heuristics written by us becomes unviable compared to the original bot.
Below there is a bar-chart of distances from the original ratio of points scored by the bots compared to random.
