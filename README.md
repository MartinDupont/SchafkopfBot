# SchafkopfBot

This is a pet project of mine; an AI agent for playing the cult bavarian card game Schafkopf, which translates literally as "sheeps head".

I decided to tackle this project because I play the game regularly, but also because I believe that the number of possible games in schafkopf is quite small, as it is bounded above by 32 factorial (~2.6e+35), which is much smaller than chess or go. This should make the game quite easy to solve using search, and so would be a good problem for me to try out my AI skills. 


## Rules of Schafkopf

Schafkopf is a deterministic, imperfect-infromation, multiplayer game for exacly four players. It is a trick-taking card game, and is closely related to the game Skat.

Schafkopf is hard to learn. Fortunately, there are many resources online detailing the rules of the game, although few are in English. The following sites should be useful:

- https://en.wikipedia.org/wiki/Schafkopf
- https://www.schafkopfschule.de/index.php/regeln.html
- https://www.sauspiel.de/schafkopf-lernen

The second link contains the official rules of the game, with a bad english translation. The wikipedia page is perhaps the most informative for an english speaker. 

In schafkopf, one has a deck of 32 cards, each having one of the suits:
- Gras ("Grass")
- Schellen ("Shells")
- Eichel ("Acorn")
- Truempfe ("Trumps")

Each player is dealt 8 cards, and 8 rounds are played in total, in which each of the players plays exactly one card. The player who plays the highest card in each round wins that hand, and wins the point value of each card played. The objective is to win as many points as possible. 

The player who plays first may play any card they want, and subsequent players must play cards of the same suit if they have them, or else, they many play anything they like. Any trump card will beat any non-trump card. The winner of the round then gets to choose the first card for the next round. 

The fact that players must follow the first card, and the fact that all cards eventually get played, means that the game has a heavy emphasis on card-counting. It is vital to keep track of who has played what, which can be quite difficult at times. This also means that a computer agent could easily have a strong advantage. 

The rules for schafkopf are far more detailed than this, and the reader should consult one of the above links if they are interested. There are a number of different game modes, which change which cards are considered trumps, and in particular, there is the partner game, in which one plays on a team with another player posessing a certain ace, although this person may not reveal themselves until the ace has been played. This presents a number of interesting computational challenges, and adds a layer of richness to the game. 

## Instructions for Use

To run a game, one must make an instance of an Arena class found in environments.py. There are two classes: Arena and HumanInterface. 

The base Arena class is designed to play four computer agents against each other. Once the arena class has been set up, rounds are played by calling new_game(), which will automatically instantiate and play a new game. A running points tally is kept between games, and the computer agents remain instantiated between games too. 

HumanInterface inherits from Arena, and is designed for playing a computer agent against four human players sitting at a card table. Running new_game() will start an interactive prompt, where the user tells the computer which cards the human opponents have played, and the agent then plays its cards at the appropriate time. 

Alternatively, one can run the parallel_matches function in multirounds.py, which runs large amounts of games across multiple CPU's.  

## AI Algorithms.

As of the 4th of october, I have two main AI agents which both perform roughly equally well. Both are based on Monte-Carlo Tree Search (MCTS) methods (see https://en.wikipedia.org/wiki/Monte_Carlo_tree_search). At present, I have not implemented an AI which "learns" in any way. The two agents are:

### MonteCarloPlus

This algorithm is based on a modified version of a classical MCTS algorithm, which I have modified for imperfect-information games in a somewhat hacky way. We calculate the MCTS tree as usual, except, when it is time for the opponents to play, we don't know what cards they have. From the game history, we can exclude that they have certain suits, but in general we cannot conclusively determine what cards they have. So, in the search tree, we assume that our opponents can play any possible card which isn't illegal or inconsistent with the game history. 

This has a number of interesting side effects. Firstly, during the tree search, the AI agent assumes his opponents will always play the card that is absolutely most inconvenient for the AI, even if it is very unlikely that the opponent actually has that card. The second, is that the branching factor becomes very large. If the AI starts the game, then he may play any of 8 cards, but the second player may play any of the 24 remaining cards, the third any of 23.. and so on. The branching factor in the early game is thus 8*24*23*22 for a single hand, which is rather large. Running on my personal computer, giving the agent two seconds to make a choice means that he can often only search 5 plies deep in the first move, which makes him quite close to useless in the early game.

### Perfect Information Monte Carlo

PIMC (http://web.cs.du.edu/~sturtevant/papers/pimc.pdf) is a modification of MCTS for imperfect information games. The algorithm, at first sight, does not seem particularly sensible. However, it performs suprisingly well on many games, and works particularly well for Skat, to which schafkopf is closely related. 

The premise is as follows: Instead of constructing a single MCTS tree, one generates a sample of possible worlds which are consistent with the game history, with each player having a known hand. Then, in each of these worlds, run a MCTS search with all players knowing each others hands. The chosen action is the action that has the highest probability of winning in each possible world. 

This algorithm has the advantage that the branching factor is significantly reduced. However, the notable disadvantage is that the simulated games often do not resemble a real game of schafkopf, and the agent has no chance of ever understanding signalling or information-sharing strategies. 

This agent also prunes the search tree by not considering cards that are equivalent. If a player has two sequential cards in his hand, say a S9 and an S8, it doesn't make any difference which one he plays, because they have the same point value, and there is no card that can beat an S9 but not an S8, and also vice-versa. This also holds for cards that have already been played. If I have the Eichel Ober and a Herz Ober (The highest and third-highest trumps), and the Gras Ober (second highest) has already been played, then I am in possession of the highest two remaining trumps and they are thus equivalent. The benefits of this pruning are marginal however. 


### Notes on the AI agents. 

Implementing the bidding phase had to be done heuristically. Running a search strategy to decide which game mode to bid for would not be particularly practical, as both my agents would have to simulate full hypothetical games, and decide which game mode has the highest chance of winning given his cards. We know that due to the high branching factor, the agent is not particularly useful in the early game, so this would not lead to good bidding strategies. 

Both the agents rely on some complicated card counting to assign valid hands to players given the game history. The math is nontrivial, so I will provide a writeup that explains how I distribute plausible hands to players. 

Both AI agents peform roughly equally well. Both have the same bidding algorithm however. 

Both the Agents have a massive advantage over a randomly-playing agent, however neither play near human level.

# Current Limitations.

Implementing the bidding phase had to be done heuristically, which is not Ideal. Especially since choosing the right game to play is far more important than playing the game itself. An agent with Heuristic bidding, which plays randomly, has a huge advantage over agents which bid and play randomly.

The agents don't learn. The goal is to eventually implement a reinforcement learning agent, once I learn more about RL and find some free time. I will start with learning on the bidding phase, as this represents a much easier problem than learning on the full game. 

The search strategies could probably still be optimized a lot. At the moment, both my search algorithms try almost all possible moves, even clearly bad ones. 
