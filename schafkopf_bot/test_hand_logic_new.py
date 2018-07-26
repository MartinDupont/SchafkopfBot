# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 17:28:46 2018

@author: martin
"""

import unittest

from gamestate import GameState

class CheckDavonlaufen(unittest.TestCase):
    def setUp(self):
        self.gamemode = "Partner Eichel"
        self.hand = ["E7_", "E8_", "E9_" ,"EA_","S7_"]
        self.state = GameState(game_mode = self.gamemode, offensive_team = (0,1), active=0)
    
    def test_open_davonlaufen(self):
        allowed = self.state.actions(self.hand)
        self.assertEqual(allowed, self.hand)
        
    def test_follow(self):
        new_state = self.state.result("E10")
        allowed = new_state.actions(self.hand)
        expected = ["EA_"]
        self.assertEqual(allowed, expected)
        
    def test_open_normal(self):
        self.hand.remove("E9_")
        allowed = self.state.actions(self.hand)
        expected = ["EA_","S7_"]
        self.assertEqual(allowed, expected)
    
    def test_follow_not_called(self):
        new_state = self.state.result("G10")
        allowed = new_state.actions(self.hand)
        expected = ["E7_","E8_", "E9_" ,"S7_"]
        self.assertEqual(allowed, expected)
        
#class CheckFullRound(unittest.TestCase):
#    hand_1 = deck[0:8]
#hand_2 = deck[8:16]
#hand_3 = deck[16:24]
#hand_4 = deck[24:]
#player_dict = {0:hand_1, 1:hand_2, 2:hand_3, 3:hand_4}
#state = GameState(game_mode="Herz Solo", offensive_team=(1,None), active=1)
#for i in range(8):
#    print(state.history)
#    for j in range(4):
#        hand = player_dict[state.active]
#        possible = state.actions(hand)
#        chosen = random.choice(possible)
#        state = state.result(chosen)
#        hand.remove(chosen)
#    print(state.history)
#    print(state.calculate_round_winner(state.history[-16:]))
#print(state.utilities())

      
if __name__ == "__main__":
    unittest.main()