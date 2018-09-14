# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:23:54 2018

@author: martin
"""
from .base_bot import BaseBot
import random

class DumbBot(BaseBot):
    """ Just plays randomly."""
            
    def play_or_not(self, previous_bids=[]):
        options = [True, False]
        return random.choice(options)
    
    def play_with(self, previous_bids=[]): 

        allowed = self.allowable_partner_games(self.hand)
                
        return random.choice(['Wenz', 'Herz Solo', 'Gras Solo', 'Eichel Solo',
                              'Schellen Solo'] + allowed 
                                + allowed
                                + allowed
                                + allowed
                                + allowed
                                + allowed
                                + allowed)

                                # cheap way of making sure they don't just play
                                # solos all the time. 
    
        
    #---------------------------------------------------------------------
    def play_card(self, state):
        card = random.choice(state.actions(self.hand))
        self.hand.remove(card)
        return card
