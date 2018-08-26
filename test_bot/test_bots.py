# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 22:12:47 2018

@author: martin
"""

import unittest

from gamestate import GameState
from bots import BaseBot, DumbBot, HeuristicBot
from MCTSPlus import MonteCarloPlus
import constants as con

class Check_BaseBot(unittest.TestCase):
    def setUp(self):
        self.bot = BaseBot()
    
    def test_basebot(self):
        self.bot.hand = ['G7_', 'HO_', 'EO_', 'GU_', 'HU_', 'SA_', 'GK_', 'EK_']
        result = self.bot.aces_in_hand()
        expected = ["SA_"]
        self.assertEqual(result, expected)
        
    def test_input(self):
        junk_hand = ["hg", "AO_"]
        with self.assertRaises(ValueError): 
            self.bot.hand = junk_hand
            
    def test_allowable_partners_1(self):
        hand = ["EO_", "EU_", "H8_", "H9_", "EA_", "G7_", "G8_", "SA_"]
        result = set(self.bot.allowable_partner_games(hand))
        expected = {"Partner Gras"}
        self.assertEqual(expected, result)
        
    def test_allowable_partners_2(self):
        hand = ["EO_", "EU_", "H8_", "H9_", "E7_", "G7_", "G8_", "SA_"]
        result = set(self.bot.allowable_partner_games(hand))
        expected = {"Partner Gras", "Partner Eichel"}
        self.assertEqual(expected, result)

    def test_allowable_partners_3(self):
        hand = ["EO_", "EU_", "H8_", "H9_", "S7_", "S8_", "S9_", "SA_"]
        result = set(self.bot.allowable_partner_games(hand))
        expected = set()
        self.assertEqual(expected, result)        

    
class Check_DumbBot(unittest.TestCase):
    def setUp(self):
        self.bot = DumbBot()
        self.bot.hand = ['G7_', 'HO_', 'EO_', 'GU_', 'HU_', 'SA_', 'GK_', 'EK_']
        game_mode = "Herz Solo"
        self.state = GameState(game_mode = game_mode, offensive_player = 0, active=0)
        
    def test_play(self):
        state = self.state.result("E10")
        action = self.bot.play_card(state)
        expected = "EK_"
        self.assertEqual(action, expected)
        
    def test_play_or_not(self):
        result = self.bot.play_or_not(0)
        self.assertTrue(result in [True, False])
        
    def test_play_with(self):
        result = self.bot.play_with(0)
        self.assertTrue(result in con.GAME_MODES)
        
        
        
class Check_HeuristicBot(unittest.TestCase):
    def setUp(self):
        self.bot = HeuristicBot()
        self.hand_1 = ["GO_", "HO_", "E7_", "E8_", "E9_", "E10", "EA_", "EK_"]
        self.hand_2 = ["GU_", "HU_", "EA_", "E10", "EK_", "EO_", "E9_", "E8_"]
    
    def test_wins_1(self):
        result, _ = self.bot.guaranteed_wins("Herz Solo", self.hand_1)
        expected = 1
        self.assertEqual(result, expected)
        
    def test_wins_2(self):
        result, _ = self.bot.guaranteed_wins("Eichel Solo", self.hand_1)
        expected = 2
        self.assertEqual(result, expected)
        
    def test_wins_3(self):
        result, _ = self.bot.guaranteed_wins("Wenz", self.hand_2)
        expected = 1
        self.assertEqual(result, expected)
        
    def test_win_wenz(self):
        """ With this hand he is guaranteed to lose one round to the Eichel 
        unter, and then win every round after that, if he gets to come out."""
        score = self.bot.win_wenz(self.hand_2)
        expected = 7
        self.assertEqual(score, expected)
        
        
    def test_to_play_1(self):
        " hand_2 is clearly the best choice for a Wenz, as opposed to a solo."""
        choice = self.bot.to_play(self.hand_2)
        expected = "Wenz"
        self.assertEqual(choice, expected)
        
    def test_to_play_2(self):
        " According to the heuristic, playing a partner schellen would be the best option"
        hand_3 = ["EO_", "EU_", "H8_", "H9_", "S7_", "G7_", "G8_", "EA_"]
        choice = self.bot.to_play(hand_3)
        expected = "Partner Schellen"
        self.assertEqual(choice, expected)  
        
    def test_to_play_3(self):
        " According to the heuristic, playing a partner schellen would be the best option"
        hand_4 = ["EO_", "EU_", "H8_", "H9_", "EA_", "G7_", "G8_", "SA_"]
        choice = self.bot.to_play(hand_4)
        expected = "Partner Gras"
        self.assertEqual(choice, expected) 

if __name__ == "__main__":
    unittest.main()