# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 14:49:51 2018

@author: martin
"""

import constants as con
import copy
from random import shuffle
from bots import DumbBot, ProxyBot
from gamestate import GameState, ReadableState

agents_dict = {"DUMB":DumbBot, "PROXY": ProxyBot}


class Arena:
    def __init__(self, bots_list, comes_out=0):
        self.agents = {}
        self.comes_out = comes_out
        if not(len(bots_list) == 4):
            raise ValueError("Please provide a string of bot names of length 4")
            
        for i, bot_string in enumerate(bots_list):
            try:
                self.agents[i] = agents_dict[bot_string]()
            except KeyError:
                raise ValueError("Not a valid bot name")
                
            # make a dictionary of agents and player instances

        self.deck = copy.deepcopy(con.ALL_CARDS)
        self.points_totals = {0:0, 1:0, 2:0, 3:0}
    
    def deal_cards(self):
        """ Deal cards to the players. This is overriden in the human interface,
            as the cards belonging to the other players are not known."""
        shuffle(self.deck)
        for i in [(self.comes_out + i) % 4 for i in range(4)]:
            self.agents[i].reset()
            self.agents[i].hand = self.deck[i*8:(i+1)*8]
        
    def new_game(self):
        """ Set up a new game, and then play each hand using play_game. """
        self.deal_cards()
        
        will_play = []
        for i in range(4):
            if self.agents[i].play_or_not():
                will_play += [i]
                
        if not will_play:
            game_mode = "Ramsch"
            offensive_player = None
            print("We are playing a Ramsch")
        else:
            prefs = []
            for i in will_play:
                preference = self.agents[i].play_with(i)
                print('Player {} wants to play a {}'.format(i, preference))
                prefs += [(i, preference)]
            final_choice =  max(prefs, key = lambda x: con.GAME_PRIORITY[x[1]])
            # in case of a tie, max returns the first maximum encountered, 
            # Thus preserving the correct order of preferences. 
            offensive_player = final_choice[0]
            game_mode = final_choice[1]

            print('Player {} is playing a {}'.format(*final_choice))        
            
        state = GameState(game_mode = game_mode,
                          offensive_player = offensive_player,
                          active = self.comes_out)
        
        self.play_game(state)
        self.comes_out = (self.comes_out+1)%4
        
    def play_game(self, state):
        """ Takes a prepared game_state object and plays rounds to completion.
        Is overridden in the human interface class."""
        for i in range(32):
            active = state.active
            card = self.agents[active].play_card(state)
            state = state.result(card)
        
        verbose = True
        if verbose:
            printable = ReadableState.from_state(state)
            print(printable)
        # update points totals.

class HumanInterface(Arena):
    """ Version of the arena that is used to play a chosen robot against 3 other
    human players at a card table. Has an interactive input feature."""
    def __init__(self, bot_name, p=0):
        b_list = []
        for i in range(4):
            if i == p:
                b_list += [bot_name]
            else:
                b_list += ["PROXY"]
        self.real_player = p
        super().__init__(b_list)

        
    # must override player initializaition.
    # and new_game, because we can't deal out peoples cards
    # play_round must be altered to print out what the bot is doing. 
    
    def deal_cards(self):
        for i in range(4):
            self.agents[i].reset()
            if i == self.real_player:
                while True:
                    input_string = input("Please type in your hand as a space-separated list of card identifiers: ")
                    cards = input_string.strip().split(" ")
                    card_list = []
                    for c in cards:
                        if len(c) == 2:
                            c += "_"
                        card_list += [c]
                    try:
                        self.agents[i].hand = card_list
                        break
                    except ValueError:
                        print("Those were not valid cards")
                        continue
                
    def play_game(self, state):
        for i in range(8):
            print("===== New Round =====")
            for j in range(4):
                active = state.active
                card = self.agents[active].play_card(state)
                print("Player {} played a {}".format(active, card))
                state = state.result(card)
            winner, points = state.calculate_round_winner()
            print("Player {} won the round, gaining {} points".format(winner, points))
        
        
        verbose = True
        if verbose:
            printable = ReadableState.from_state(state)
            print(printable)
        # update points totals.
            
        

    