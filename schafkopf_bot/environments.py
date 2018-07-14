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
        self.game_state = np.zeros((4, 4, 8, 32), dtype=int)
        # This encoding does keep track of play order, although it is a little sparse
        self.game_mode = None # should be a one-hot encoding of lenght(game_modes)
        self.whos_playing = None # should be a binary vector of length 4
        self.round = 1
        
        self.players = None #Some object which stores players. Make a bunch of players
        self.deck = copy.deepcopy(con.ALL_CARDS)
        self.comes_out = 0
        self.player_points = {0:0, 1:0, 2:0, 3:0}
        
    def new_game(self):
        raise NotImplementedError()
        
    def play_round(self):
        raise NotImplementedError()
            
        
    def make_state_vector(self, player_num):
        # gotta figure out whether I want player_num to be actual number 
        # or position in the queue.
        
        linearized = np.roll(self.game_state, -player_num,  axis = 0).ravel()
        state_vector = np.concatenate((linearized, self.game_mode, self.whos_playing))
        return state_vector
        
    
    def round_representation(game_state, round_num):
        # should these be inside or outside the class?
        cards_played = game_state[:, :, round_num, :]
        thing= np.where(np.sum(cards_played, axis =2))
        thing_2 = [(i,j,con.vec_2_cards(cards_played[i, j]))
                for i,j in zip(*thing)]
        
        thing_3 = sorted(thing_2, key=lambda x: x[0])
        
        readable_cards_played = [(b, c) for a, b, c in thing_3]
        return readable_cards_played

    def game_representation(game_state):
        rep = dict()
        for i in range(1, 9):
            rep[i] = self.round_representation(game_state, i-1)
        return rep


        
    def calculate_round_winner(self, round_num):        
        readable_cards_played = self.round_representation(self.game_state, round_num)
        if len(readable_cards_played) != 4:
            raise ValueError("Round {} has not been played to completion".format(round_num))
            
        # gotta check if it's (player,card) or (card, player)
        
        suit = self.suit_dictionary[readable_cards_played[0][0]]

        trumps = [tup for tup in 
                  readable_cards_played if self.suit_dictionary[tup[0]] == "Truempfe"]

        if trumps:
            winning_player =  sorted(trumps, key=lambda x:
                            self.trump_ordering.index(x[0]),reverse=True)[0][1]
            # extract the player number
        else:
            # If no trumps, the highest card matching the suit will win. 
            correct_suit_cards = [tup for tup in readable_cards_played
                                  if self.suit_dictionary[tup[0]] == suit]
            winning_player = sorted(correct_suit_cards, key= lambda x:
                self.card_ordering.index(x[1::]), reverse=True)[0][1] 
            
        points = sum(con.Points[c] for c, p in readable_cards_played)
        return winning_player, points
        
        
    
    def calculate_game_winner(self):
        offensive_team = self.whos_playing
        defensive_team = [p for p in range(4) if not p in offensive_team]

        offensive_points = 0    
        defensive_points = 0

        for p, points in self.player_points:
            if p in offensive_team:
                offensive_points += points
#            else:
#                defensive_points += points
        
        if offensive_points >= 61:
            return offensive_team
        else:
            return defensive_team
        # This actually needs way more work.
        # For now, I can just do a win/lose, but ideally, I want to win  
        # and lose by a certain number of points, AND i want laufenden and haxen etc. 


        

class HumanInterface(Arena):
    def __init__(self, bot, p=0):
        self.players[p] = DumbBot()
        for i in range(4):
            if i != p:
                self.players[i] = ProxyBot()
        
    # must override player initializaition.
    # and new_game, because we can't deal out peoples cards
    # play_round must be altered to print out what the bot is doing. 
    
    def new_game(hand , p=0):
        for i in range(4):
            self.players[i].give_hand(hand)
                # None of the ProxyBot's methods should actually check what hand he has....
        

class AllRobots(Arena):
    def __init__():
        super()__init__()
        self.players = {i:DumbBot() for i in range(4)}
        
    def new_game(self):
        self.round = 0
        self.game_state = np.zeros((4, 4, 8, 32), dtype=int)
        self.player_points = {0:0, 1:0, 2:0, 3:0}
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
        #feed these to the bots
        
    def play_round(self):
        # the continuous playing loop should not be done here. 
        for i,p in enumerate(self.play_order):
            player = self.players[p]
            card_num = player.play_card(self.make_state_vector(p))
            self.game_state[i, p, self.round, card_num] = 1
        
        winner, points = self.calculate_round_winner(self.game_state, self.round)
        self.player_points[winner] += points
        self.play_order = con.make_play_order(winner)
        
        self.round += 1
        if self.round == 8:
            self.calculate_game_winner()

    # Need something which is capable of setting up a single bot and letting
    # me put in commands manually.
    
    
class SimulationArena(Arena):
    # like arena, but can start playing rounds when halfway through. 
    