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

Costwise, the time-, and-space-complexity of calculating one particular potential move did not significantly increase with either options, so the only measurable factor remains
