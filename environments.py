# -*- coding: utf-8 -*-
"""
This file contains the environments, which are responsible for loading 
multiple agents, dealing them cards, and conducting the bidding process
for deciding which game to play. They also run the games.
"""

import constants.constants as con
from random import shuffle
from bots import DumbBot, ProxyBot, HeuristicBot, MonteCarloBot, MonteCarloPointsBot, PerfectInformationMonteCarloBot
from gamestate import GameState

agents_dict = {"DUMB":DumbBot, "PROXY": ProxyBot, "HEURISTIC": HeuristicBot,
               "MCTSPLUS":MonteCarloBot, "POINTS":MonteCarloPointsBot,
               "PIMC":PerfectInformationMonteCarloBot}


class Arena:
    """ This class is the overarching environment. It is responsible for setting
    up a game with a fixed set of players. Multiple games can be played, and
    the players remain instantiated between games. It asks the players what 
    type of game they would like to play, then creates the appropriate GameState
    instance."""
    def __init__(self, bots_list, comes_out=0):
        """ bots_list is a list of lists, [["PIMC", kwargs], ["DUMB", kwargs], ...] """
        self.agents = {}
        self.comes_out = comes_out
        if not(len(bots_list) == 4):
            raise ValueError("Please provide a string of bot names of length 4")
        
        # make a dictionary of agents and player instances
        for i, bot_params in enumerate(bots_list):
            try:
                self.agents[i] = agents_dict[bot_params[0]](**bot_params[1])
            except KeyError:
                raise ValueError("{} is not a valid bot name".format(bot_params[0]))
                
        self.deck = list(con.ALL_CARDS)
        self.points_totals = {0:0, 1:0, 2:0, 3:0}
    
    def deal_cards(self):
        """ Deal cards to the players. This is overriden in the human interface,
            as the cards belonging to the other players are not known."""
        shuffle(self.deck)
        for i in [(self.comes_out + i) % 4 for i in range(4)]:
            self.agents[i].reset()
            self.agents[i].hand = self.deck[i * 8: (i + 1) * 8]  
        
    def who_will_play(self):
        """ Asks each player in order if they would like to play. 
        Each player is informed whether the previous players have shown an 
        interest in playing."""
        will_play = []
        bid_order = [(self.comes_out + i) % 4 for i in range(4)]
        for i in bid_order:
            will_play += [(i, self.agents[i].play_or_not(will_play))]
        return will_play
    
    def decide_game_mode(self, will_play, verbose=False):
        if not any(x[1] for x in will_play):
            game_mode = "Ramsch"
            offensive_player = None
        else:
            prefs = []
            for i, t in will_play:
                # will_play is ordered by who bid first
                if t:
                    preference = self.agents[i].play_with(prefs)
                    prefs += [(i, preference)]
                else:
                    prefs += [(i, None)]
        
            offensive_player, game_mode =  max(prefs, key = lambda x: con.GAME_PRIORITY[x[1]])
            
        if verbose:
            print("=========== Bidding Phase ===========")
            if game_mode == "Ramsch":
                print("Nobody wanted to play.")
            else:
                for i, preference in prefs:
                    if not preference is None:
                        print('Player {} wanted to play a {}'.format(i, preference))
            
        return game_mode, offensive_player
    
        
    def play_game(self, state, verbose):
        """ Takes a prepared game_state object and plays rounds to completion.
        Is overridden in the human interface class."""
        for i in range(32):
            active = state.active
            card = self.agents[active].play_card(state)
            state = state.result(card)
        
        game_points = self.winner_game_points(state.utilities())
        for i in range(4):
            self.points_totals[i] += game_points[i]
        if verbose:
            print(state)
        # update points totals.
        
        
    def winner_game_points(self, utils):
        """ The amount of points players win by winning one game is NOT the 
        same as the number of points which they won from cards during the game. 
        A separate points tally is maintained between rounds, which is designed
        such that the points between rounds are zero-sum, and thus the game may
        be played for money."""
        n_winners = sum(utils)
        if n_winners == 1:
            win_points = 3
            lose_points = -1
        
        elif n_winners == 2:
            win_points = 1
            lose_points = -1
        elif n_winners == 3:
            win_points = 1
            lose_points = -3
        else:
            raise ValueError("Sum of utilities was not 1,2, or 3, sum = {}".format(utils))
        
        results = tuple(win_points if i == 1 else lose_points for i in utils)
        return results
            
    def new_game(self, verbose=True):
        """ Set up a new game, by deciding which type of game is to be played,
        and then play each game to completion. """
        self.deal_cards()
        
        will_play = self.who_will_play()
        
        game_mode, offensive_player = self.decide_game_mode(will_play, verbose)
            
        state = GameState(game_mode = game_mode,
                          offensive_player = offensive_player,
                          active = self.comes_out)
        
        self.play_game(state, verbose)
        self.comes_out = (self.comes_out + 1) % 4

class HumanInterface(Arena):
    """ Version of the arena that is used to play a chosen robot against 3 other
    human players at a card table. Has an interactive input feature."""
    def __init__(self, bot_name, p=0, comes_out =0 ):
        b_list = []
        for i in range(4):
            if i == p:
                b_list += [bot_name]
            else:
                b_list += ["PROXY"]
        self.robot_player = p
        super().__init__(b_list, comes_out)

        
    # must override player initializaition.
    # and new_game, because we can't deal out peoples cards
    # play_round must be altered to print out what the bot is doing. 
    def who_will_play(self):
        will_play = []
        bid_order = [(self.comes_out + i) % 4 for i in range(4)]
        for i in bid_order:
            choice = self.agents[i].play_or_not(will_play)
            will_play += [(i, choice)]
            
            if i == self.robot_player:
                if choice:
                    print("Player {} would like to play.".format(i))
                else:
                    print("Player {} would not like to play.".format(i))
        return will_play    
    
    
    
    def deal_cards(self):
        for i in range(4):
            self.agents[i].reset()
            if i == self.robot_player:
                while True:
                    input_string = input("Please type in your hand as a space-separated list of card identifiers: ")
                    cards = input_string.strip().upper().split(" ")
                    card_list = []
                    for c in cards:
                        if len(c) == 2:
                            c += "_"
                        card_list += [c]
                    try:
                        self.agents[i].hand = card_list
                        break
                    except ValueError as e:
                        print(e.args)
                        continue
                
    def play_game(self, state, verbose = True):
        for i in range(8):
            print("===== New Round =====")
            for j in range(4):
                active = state.active
                card = self.agents[active].play_card(state)
                print("Player {} played a {}".format(active, card))
                state = state.result(card)
                self.state = state
            winner, points = state.calculate_round_winner()
            print("Player {} won the round, gaining {} points".format(winner, points))
        
        if verbose:
            print(state)
            

    