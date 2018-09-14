# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:22:51 2018

@author: martin
"""
from constants import constants as con
import copy

class BaseBot():
    def __init__(self):
        self._hand = None
    
    def reset(self):
        self.hand = None
    # ------------------------------------------------
    def get_hand(self):
        return self._hand
    
    def set_hand(self, hand): 
        if not (hand is None):
            if not all([a in con.ALL_CARDS for a in hand]):
                raise ValueError("These aren't valid cards")
            l_s_h = len(set(hand))
            l_h = len(hand)
            if l_s_h != l_h:
                raise ValueError("You may have given me duplicate cards. "
                                 "len(set(hand)) = {}, len(hand) = {}".format(l_s_h, l_h))
            if l_s_h != 8:
                raise ValueError("You only gave me {} card(s).".format(l_s_h))
        self._hand = copy.deepcopy(hand)
    hand = property(get_hand, set_hand)
    # -------------------------------------------       
    def allowable_partner_games(self, hand):
        if not len(hand) == 8:
            raise ValueError("Not a full hand.")
        
        suit_map = con.STANDARD_MAPPING
        suits = set(suit_map[a] for a in hand if suit_map[a] != 'Truempfe')
        for card in hand:
            if card in ['SA_', 'EA_', 'GA_']: # can't play with an ace that you have
                suits.remove(suit_map[card])
                
        allowed = ["Partner "+s for s in suits] # valid even if suits is empty.
        return allowed
      
    def aces_in_hand(self):
        return [a for a in self.hand if a[1] == 'A']

    def play_card(self, state):
        raise NotImplementedError
    
    def play_or_not(self):
        raise NotImplementedError
    
    def play_with(self):
        raise NotImplementedError