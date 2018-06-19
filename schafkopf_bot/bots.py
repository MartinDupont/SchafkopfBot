# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 12:42:28 2018

@author: martin
"""

import random
import copy
import numpy as np
import constants as con

class DumbBot:
    def __init__(self, hand):
        self.hand = None
        
    def make_state_vector(self, input_state):
        """Accepts linearized numpy array from the Arena. Appends its own vectorized
        hand to the input_state"""
        state_vector = np.append(input_state, self.hand)
        return state_vector
    
    def reset(self):
        self.hand = None

    def give_hand(self, hand):
        # Perhaps I want to have polymorphism here or whatever. Can accept
        # either a list of strings or a vector. 
        if not all([a in con.ALL_CARDS for a in hand]):
            raise ValueError("These aren't valid cards")
        else:
            self.hand = con.cards_2_vec(hand)      
            
class GameModeBot(DumbBot):
    def __init__(self):
        pass
    # Make the robot only learn on games in which they actually play the 
    # game mode that he selected (1st approximation)
    