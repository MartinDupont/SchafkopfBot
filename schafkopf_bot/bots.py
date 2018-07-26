# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 12:42:28 2018

@author: martin
"""

import random
import copy
import numpy as np
import constants as con

class BaseBot():
    def __init__(self):
        self.hand = None

    def make_state_vector(self, input_state):
        
        """Accepts linearized numpy array from the Arena. Appends its own vectorized
        hand to the input_state"""
        state_vector = np.append(input_state, self.hand)
        return state_vector
    
    def reset(self):
        self.hand = None
        self.card_ordering = None
        self.trump_ordering = None
        self.called_ace = None
        self.suit_dictionary = None 

    def give_hand(self, hand):
        # Perhaps I want to have polymorphism here or whatever. Can accept
        # either a list of strings or a vector. 
        if not all([a in con.ALL_CARDS for a in hand]):
            raise ValueError("These aren't valid cards")
        else:
            self.hand = con.cards_2_vec(hand) 
            
            
    def aces_in_hand(self):
        return [a for a in self.hand if a[1] == 'A']

    def set_game_mode(self, game_mode):
        #TODO: this should probably be shifted to the State.
        if not game_mode in con.GAME_MODES:
            raise ValueError("{} is not a valid game mode".format(game_mode))
        self.card_ordering, self.trump_ordering, self.called_ace, self.suit_dictionary = con.constants_factory(game_mode)
 
# =========================================================================== # 
class DumbBot(BaseBot):

            
    def play_or_not(self):
        options = ['spiele', 'spiele nicht']
        return random.choice(options)
    
    def play_with(self): 
        my_aces = self.aces_in_hand()
        allowable_partner_games = {self.suit_dictionary[c] for c in self.hand if not
                                   (c in my_aces and self.suit_dictionary[c] != "Truempfe")}
        
        temp = ["Partner " + s for s in allowable_partner_games] # valid even if suits is empty.
        
        return random.choice(['Wenz', 'Herz Solo', 'Gras Solo', 'Eichel Solo',
                              'Schellen Solo'] + temp + temp + temp) 
    
        
    #---------------------------------------------------------------------
    def calculate_legal_moves(self, game_state, round_num):
        
        # need access to round_representation here 
        # all of this internal shit, card_ordering, trump_ordering, should
        # go in the state and get pulled from the state when needed. 
        
        
        if len(self.hand) == 1:
            return self.hand   
        
        matching_cards = [card for card in self.hand if self.getSuits(card) == self.currentSuit]
        # If I can't match the suit, play whatever. Also works if I'm coming out.
        if not(matching_cards):
            matching_cards = self.hand
        
        # check if we're playing a partner game, and I have the called ace. 
        if self.gameMode in ['Partner Schellen','Partner Eichel','Partner Gras'] and (con.GAME_MODE_TO_ACES[self.gameMode] in self.hand): ## if we're doing a partner play
            called_colour = self.gameMode.split(' ')[1]
            called_ace =con.GAME_MODE_TO_ACES[self.gameMode]
            if self.playedThisRound:
                if self.currentSuit == called_colour:
                    # play the ace if I have it
                    return [called_ace]
                else: 
                    # play any valid card that isn't the ace
                    return [card  for card in matching_cards if card != called_ace] 
            else: 
                # If i am allowed to come out.
                if len([card for card in self.hand if self.getSuits(card) == called_colour]) >= 4:
                    # can "run away" and not open with the ace. 
                    return self.hand
                else:
                    # Can open with the called ace, but not any other card of the called colour
                    return [card  for card in self.hand if 
                            (card == called_ace) or (self.getSuits(card) != called_colour)]  
            
        return matching_cards

       
                
    def play_card(self):
        play = self.playRandom()
        return play

    def play_random(self): 
        # This still assumes that the hand is a list not a vector
        if self.gameMode == None:
            print('we havent set the gamemode yet!')
            return None
        if self.hand == []:
            print('No cards left in hand')
            return None
        available = self.calculateLegalMoves()
        play = random.choice(available)
        self.setPlayedCard(play)
        self.hand.remove(play) 
        self.currentSuit == None
        return play  
    
    def force_play(self,card):
        # TODO: This still assumes that the hand is a list not a vector.
        if not (card in self.hand):
            print('That card is not in my hand')
            return None

        self.setPlayedCard(card)
        self.hand.remove(card) 
    
        return card    
 

class ProxyBot(BaseBot):
    
    def play_card(self, state):
        # figure out from the state what his player number is.
        play = input("Which card would you like to play?: ")
        if not play in con.ALL_CARDS:
            raise ValueError("{} is not a valid card")



           
class GameModeBot(DumbBot):
    def __init__(self):
        pass
    # Make the robot only learn on games in which they actually play the 
    # game mode that he selected (1st approximation)
    