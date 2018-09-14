# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:25:48 2018

@author: martin
"""
import constants as con
from .base_bot import BaseBot


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

    def play_or_not(self, previous_bids=[]):
        i = len(previous_bids)
        play = input("""Would player {} like to play?: \n1: Play \n2: Don't play \n""".format(i))
        if play == "1":
            return True
        return False
    
    def play_with(self, previous_bids=[]):
        i = len(previous_bids)
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