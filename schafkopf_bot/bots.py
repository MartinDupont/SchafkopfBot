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
        self._hand = None

#    def make_state_vector(self, input_state):
#        
#        """Accepts linearized numpy array from the Arena. Appends its own vectorized
#        hand to the input_state"""
#        state_vector = np.append(input_state, self.hand)
#        return state_vector
    
    def reset(self):
        self.hand = None
#        self.card_ordering = None
#        self.trump_ordering = None
#        self.called_ace = None
#        self.suit_dictionary = None 
    # ------------------------------------------------
    def get_hand(self):
        return self._hand
    
    def set_hand(self, hand): 
        if not (hand is None):
            if not all([a in con.ALL_CARDS for a in hand]):
                raise ValueError("These aren't valid cards")
        self._hand = hand
    hand = property(get_hand, set_hand)
    # -------------------------------------------       
            
    def aces_in_hand(self):
        return [a for a in self.hand if a[1] == 'A']

    def play_card(self, state):
        raise NotImplementedError
    
    def play_or_not(self):
        raise NotImplementedError
    
    def play_with(self):
        raise NotImplementedError
# =========================================================================== # 
class DumbBot(BaseBot):
    """ Just plays randomly."""
            
    def play_or_not(self):
        options = [True, False]
        return random.choice(options)
    
    def play_with(self, i): 
        my_aces = self.aces_in_hand()
        suit_dictionary = con.STANDARD_MAPPING
        allowable_partner_games = {suit_dictionary[c] for c in self.hand if not
                                   (c in my_aces or suit_dictionary[c] == "Truempfe")}
        temp = ["Partner " + s for s in allowable_partner_games] # valid even if suits is empty.
        
        return random.choice(['Wenz', 'Herz Solo', 'Gras Solo', 'Eichel Solo',
                              'Schellen Solo'] + temp + temp + temp) 
    
        
    #---------------------------------------------------------------------
    def play_card(self, state):
        card = random.choice(state.actions(self.hand))
        self.hand.remove(card)
        return card
       
        

class ProxyBot(BaseBot):
    """ Plays with human input. For debugging purposes, and for playing 
    against real opponents at card tables"""
    
    def play_card(self, state):
        # Note that this function doesn't need to know the proxybot's hand. 
        # This is so that we can play against opponents whose hands we dont know.
        while True:
            play = input("Which card would player {} like to play? \n".format(state.active))
            if len(play) == 2:
                play = play + "_"
            if play in con.ALL_CARDS:
                return play
            else:
                print("{} is not a valid card".format(play))
                
        return play

    def play_or_not(self):
        play = input("""Would like to play?: \n1: Play \n2: Don't play \n""")
        if play == "1":
            return True
        return False
    
    def play_with(self, i):
        while True:
            input_string = "Player {} would like to play a: \n".format(i)
            option_dict = {}
            j = 0
            for  g in con.GAME_MODES:
                if g != "Ramsch":
                    input_string += str(j)+": "+g+"\n"
                    option_dict[j] = g
                j += 1
                
            option_dict[str(i)] = "Ramsch" 
            # Ramsch will be an option for if players misspeak (as often happens over beers),
            # such that they can elect not to play after just having played. 
            input_string += str(j)+": Cancel \n" # may or may not be necessary
            play = input(input_string)
            try:
                return option_dict[play]
            except KeyError:
                print("That is not a valid choice")
                continue
        


           
class GameModeBot(DumbBot):
    def __init__(self):
        pass
    # Make the robot only learn on games in which they actually play the 
    # game mode that he selected (1st approximation)
    