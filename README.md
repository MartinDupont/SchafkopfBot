# SchafkopfBot

This is a pet project of mine; an AI agent for playing the cult bavarian card game Schafkopf, which translates literally as "sheeps head".

I decided to tackle this project because I play the game regularly, but also because I believe that the number of possible games in schafkopf is quite small, as it is bounded above by 32 factorial (~2.6e+35), which is much smaller than chess or go. This should make the game quite easy to solve using search, and so would be a good problem for me to try out my AI skills. 


## Rules of Schafkopf

Schafkopf is a deterministic, imperfect-infromation, multiplayer game for exacly four players. 

Schafkopf is hard to learn, and there are many resources online detailing the rules of the game, although few are in English. The following sites should be useful:

- https://en.wikipedia.org/wiki/Schafkopf
- https://www.schafkopfschule.de/index.php/regeln.html
- https://www.sauspiel.de/schafkopf-lernen

The second link contains the official rules of the game, with a bad english translation. The wikipedia page is perhaps the most informative for an english speaker. 

In schafkopf, one has a deck of 32 cards, each having one of the suits:
- Gras ("Grass")
- Schellen ("Shells")
- Eichel ("Acorn")
- Truempfe ("Trumps")

Each player is dealt 8 cards, and 8 rounds total are played, in which each of the players plays exactly one card. The player who plays the highest card in each round wins that hand, and wins the point value of each card played. The objective is to win as many points as possible. 

The player who plays first may play any card they want, and subsequent players must play cards of the same suit if they have them, or else, they many play anything they like. Any trump card will beat any non-trump card. The winner of the round then gets to choose the first card for the next round. 

The fact that players must follow the first card, and the fact that all cards eventually get played, means that the game has a heavy emphasis on card-counting. It is vital to keep track of who has played what, which can be quite difficult at times. This also means that a computer agent could easily have a strong advantage. 

The rules for schafkopf are far more detailed than this, and the reader should consult one of the above links if they are interested. There are a number of different game modes, which change which cards are considered trumps, and in particular, there is the partner game, in which one plays on a team with another player posessing a certain ace, although this person may not reveal themselves until the ace has been played. This presents a number of interesting computational challenges, and adds a layer of richness to the game. 

## Instructions for Use

To run a game, one must make an instance of an Arena class found in environments.py. There are two classes: Arena and HumanInterface. 

The base Arena class is designed to play four computer agents against each other. Once the arena class has been set up, rounds are played by calling new_game(), which will automatically instantiate and play a new game. A running points tally is kept between games, and the computer agents remain instantiated between games too. 

HumanInterface inherits from Arena, and is designed for playing a computer agent against four human players sitting at a card table. Running new_game() will start an interactive prompt, where the user tells the computer which cards the human opponents have played, and the agent then plays its cards at the appropriate time. 


## Misc.

As of the 2nd of August 2018, the computer agent is still being refined and tested, so I will refrain from posting any detailed summary on how the different game playing agents work. 