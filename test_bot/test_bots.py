# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 22:12:47 2018

@author: martin
"""

import unittest

from gamestate import GameState
from bots import BaseBot, DumbBot, MonteCarlo
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
        
class Check_MCTS(unittest.TestCase):
    """ Really gotta expand this"""
    def setUp(self):
        self.bot = MonteCarlo()
        self.bot.hand = ['G7_', 'HO_', 'EO_', 'GU_', 'HU_', 'SA_', 'GK_', 'EK_']
        game_mode = "Herz Solo"
        self.state = GameState(game_mode = game_mode, offensive_player = 0, active=0)
        
    def test_play(self):
        state = self.state.result("E10")
        action = self.bot.play_card(state)
        expected = "EK_"
        self.assertEqual(action, expected)



        
#    ['SK_', 'H10', 'G10', 'E9_', 'E7_', 'S10', 'G8_', 'EA_']
#['G7_', 'HO_', 'EO_', 'GU_', 'HU_', 'SA_', 'GK_', 'EK_']
#['SO_', 'EU_', 'SU_', 'GA_', 'H7_', 'H8_', 'S8_', 'H9_']
#['S7_', 'HK_', 'E8_', 'G9_', 'GO_', 'E10', 'HA_', 'S9_']
            
if __name__ == "__main__":
    unittest.main()