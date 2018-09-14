# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:26:44 2018

@author: martin
"""
from constants import constants as con
from .dumb_bot import DumbBot

class HeuristicBot(DumbBot):
    """ Agent that uses heuristics to bid. In the future it will also 
    follow a heuristic to play whole games as well."""
    
    def guaranteed_wins(self, game_mode, hand):
        trump_ordering = con.TRUMP_ORDERINGS[game_mode]
        n_wins = 0
        n_trumps = 0
        for t in trump_ordering:
            if t in hand:
                n_wins += 1
                n_trumps += 1
            else:
                n_wins = max([0, n_wins-1])
        return (n_wins, n_trumps)
        
    
    def win_wenz(self, hand):
        """ Calculate if it's a good idea to play a Wenz. Calculates how many 
        hands one can be reasonably expected to win."""
        n_wins, _ = self.guaranteed_wins("Wenz", hand)

        n_colour_wins = 0
        aces = ["EA_", "GA_", "HA_", "SA_"]
        for ace in aces:
            n_colour_wins += self.find_runs(hand, ace)
            
        
        # This score is a bit hopeful. In assuming that he has one win from
        # the unters, he assumes that he can either draw all the unters out, 
        # and then can play all his colour cards as he pleases. 
        # This will break down if, for example, he has the eichel Unter, and 
        # one of his opponents has the other three unters. 
        if n_wins > 0:
            score = n_wins + n_colour_wins
        else:
            # Can't pull out any unters, and my high cards will all get taken.
            score = 0
        return score
    
    # ------------------------------------------------------------------------
    def find_runs(self, hand, ace):
        """ Identifies the lengths of a run of consecutive high-cards, 
        i.e. A, 10, K ... etc. These runs are guaranteed wins once the 
        Unters have all been drawn out, assuming you get to play first."""
        suit = ace[0]
        stop = False
        ordering = con.WENZ_ORDERING
        index = -1
        n = 0 
        while not stop:
            card = suit + ordering[index]
            if card in hand:
                n += 1
                index -= 1
                if index == -8:
                    stop = True
            else:
                stop = True
        return n
  
            
        
    def win_solo(self, hand, game_mode):
        """ This decides if the player is likely to win by calculating a simple
        heuristic. One can calculate how many hands you are guaranteed to win, 
        by observing how many trumps you have, and how many remaining trumps
        there are that are higher than that card. """
        n_wins, n_trumps = self.guaranteed_wins(game_mode, hand)
                
        if n_wins > 0:
            score = (n_wins + n_trumps)/2
        else:
            score = 0
        return score

    
    def to_play(self, hand, previous_bids=[], threshold = 5):
        scores = []
        for g_mode in ["Herz Solo", "Gras Solo", "Eichel Solo", "Schellen Solo"]:
            scores += [(g_mode, self.win_solo(hand, g_mode))]

        scores += [("Wenz", self.win_wenz(hand))]
        
        best = max(scores, key = lambda x: x[1]) 
        if best[1]  >= threshold: 
            return best[0]
        
        else:  
            allowed = self.allowable_partner_games(hand)
            if allowed:
                n_wins, n_trumps= self.guaranteed_wins("Herz Solo", hand) # herz solo has normal trump ordering 
                obers = ["EO_", "GO_", "HO_", "SO_"]
                unters = ["EU_", "GU_", "HU_", "SU_"]
                n_obers = len([c for c in hand if c in obers])
                n_unters = len([c for c in hand if c in unters])
                if n_trumps >= 4 and (n_obers > 0) and (n_obers+n_unters >= 2):
                    suit_map = con.STANDARD_MAPPING
                    pairs = []
                    for game in allowed:
                        suit = game.split(" ")[1] ## extracts Eichel from "Partner Eichel" etc. 
                        n_of_suit = len([c for c in hand if suit_map[c] == suit])
                        pairs += [(game, n_of_suit)]
                    best = min(pairs, key= lambda x: x[1])
                    return best[0]
                    # If one wants to play a partner game, then you should 
                    # play it with the colour that you have the least of, 
                    # because it minimizes the chances of your opponents being
                    # free in that colour when the ace is  played. 
        return False
  
    def play_or_not(self, previous_bids=[]):
        result = self.to_play(self.hand, previous_bids)
        if result:
            return True
        return False
    
    def play_with(self, previous_bids=[]):
        result =  self.to_play(self.hand, previous_bids)
        if result:
            return result
        else:
            raise ValueError("""Agent was asked what game type it wants to play, 
                             although it did not want to play.""")
