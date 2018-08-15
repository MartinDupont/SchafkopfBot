# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 12:42:28 2018

@author: martin
"""

import random
import constants as con
import math
import time
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
            
    def play_or_not(self, i):
        options = [True, True, True, False]
        return random.choice(options)
    
    def play_with(self, i): 
        my_aces = self.aces_in_hand()
        temp_dict = {"Partner Schellen": "SA_", "Partner Eichel": "EA_",
                     "Partner Gras": "GA_"}
        allowable_partner_games = [key for key, value in temp_dict.items() 
                                    if not value in my_aces]

        
        return random.choice(['Wenz', 'Herz Solo', 'Gras Solo', 'Eichel Solo',
                              'Schellen Solo'] + allowable_partner_games 
                                + allowable_partner_games 
                                + allowable_partner_games
                                + allowable_partner_games
                                + allowable_partner_games
                                + allowable_partner_games
                                + allowable_partner_games) 
                                # cheap way of making sure they don't just play
                                # solos all the time. 
    
        
    #---------------------------------------------------------------------
    def play_card(self, state):
        card = random.choice(state.actions(self.hand))
        self.hand.remove(card)
        return card
       
# =========================================================================== #        

class ProxyBot(BaseBot):
    """ Plays with human input. For debugging purposes, and for playing 
    against real opponents at card tables"""
    
    def play_card(self, state):
        # Note that this function doesn't need to know the proxybot's hand. 
        # This is so that we can play against opponents whose hands we dont know.
        while True:
            play = input("Which card would player {} like to play? \n".format(state.active))
            play = play.upper()
            if len(play) == 2:
                play = play + "_"
            if play in con.ALL_CARDS:
                return play
            else:
                print("{} is not a valid card".format(play))
                
        return play

    def play_or_not(self, i):
        play = input("""Would player {} like to play?: \n1: Play \n2: Don't play \n""".format(i))
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
                    option_dict[str(j)] = g
                j += 1
                
            option_dict[str(j)] = "Ramsch" 
            # Ramsch will be an option for if players misspeak (as often happens over beers),
            # such that they can elect not to play after just having played. 
            input_string += str(j)+": Cancel \n" # may or may not be necessary
            play = input(input_string)
            try:
                return option_dict[play]
            except KeyError:
                print("That is not a valid choice")
                continue
        