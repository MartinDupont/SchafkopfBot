# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 14:49:51 2018

@author: martin
"""
import  numpy as np
import constants as con
import copy
from random import shuffle

# internally, as much of the processing as possible should be done with the array. 

# Solution, have robot which does everything internally with arrays.

#wrap instances in a human-readable interface. 


class Arena:
    def __init__(self):
        # placeholder for players
        self.game_state = np.zeros((4,4, 8, 32), dtype=int)
        # This encoding does keep track of play order, although it is a little sparse
        self.game_mode = None # should be a one-hot encoding of lenght(game_modes)
        self.whos_playing = None # should be a binary vector of length 4
        self.round = 1
        
        self.players = None #Some object which stores players. Make a bunch of players
        self.deck = copy.deepcopy(con.ALL_CARDS)
        self.comes_out = 0
        
    def new_game(self):
        self.round = 0
        self.game_state = np.zeros((4, 4, 8, 32), dtype=int)
        self.comes_out = (self.comes_out + 1) % 4
        shuffle(self.deck)
        count = 0
        for p in self.players:
            p.reset()
            hand = self.deck[count:count+8]
            p.give_hand(hand)
            count += 8
        
        for i in range(4):
            ind = i + self.comes_out
            self.players[ind].play_or_not()
            # This function needs two steps. A bot needs to calculate if he
            # wants to play, and what he wants to play with. But the two facts
            # need to be yielded separately. 
        
        self.game_mode = thing
        self.whos_playing = other_thing
        
        card_ordering, trump_ordering, called_ace, suit_dictionary = con.constants_factory(self.game_mode)
        
    def play_round(self):
        for i,p in enumerate(play_order):
            player = self.players[p]
            card_num = player.play_card(self.make_state_vector(p))
            self.game_state[i, p, self.round, card_num] = 1
        
        winner = self.calculate_round_winner(self.game_state)
        play_order = con.make_play_order(winner)
        
        self.round += 1
        if self.round == 8:
            self.calculate_game_winner()
            self.new_game()
        
    def make_state_vector(self, player_num):
        # gotta figure out whether I want player_num to be actual number 
        # or position in the queue.
        
        linearized = np.roll(self.game_state, -player_num,  axis = 0).ravel()
        state_vector = np.concatenate((linearized, self.game_mode, self.whos_playing))
        return state_vector
        
        
    def calculate_round_winner(self, round_num):
        cards_played = self.game_state[:, :, round_num, :]
        if np.sum(cards_played) != 4:
            raise ValueError("Round {} has not been played to completion".format(round_num))
        thing = np.where(np.sum(cards_played, axis =2))
        # I'm probably going to be doing the conversion from array to strings alot
        # This should be turned into a standalone function...
        thing_2 = [(i,j,con.vec_2_cards(cards_played[i, j]))
                    for i,j in zip(*thing)]
        
        pass
    
    def calculate_game_winner(self):
        pass


class HumanInterface:
    def __init__(self):
        pass

    # Need something which is capable of setting up a single bot and letting
    # me put in commands manually.