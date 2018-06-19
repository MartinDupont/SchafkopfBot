# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 12:42:28 2018

@author: martin
"""

import random
import copy
import constants as con

class DumbBot:
    def __init__(self, hand):
        if not all([a in con.ALL_CARDS for a in hand]):
            raise ValueError("These aren't valid cards")
        else:
            self.hand = copy.deepcopy(hand)
        
        self.current_suit = None
        self.played_this_round = []
        self.played_this_game = []
        
    @property
    def game_mode(self):
        return self._game_mode
    
    @game_mode.setter
    def game_mode(self, value):
        if value in con.GAME_MODES:
            self._game_mode = value
            junk1, junk2, self.called_ace, self.suits_mapping = con.constants_factory(value)
        else:
            raise ValueError("{} is not a valid game mode".format(value))