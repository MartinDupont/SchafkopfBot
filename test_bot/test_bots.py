# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 22:12:47 2018

@author: martin
"""

import unittest

from gamestate import GameState
from bots import BaseBot, DumbBot
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
        

if __name__ == "__main__":
    unittest.main()