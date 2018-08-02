# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:46:12 2018

@author: martin
"""

import unittest
from MCTSPlus import inverse_legal_moves, how_many, assign_hands
from distribute_cards import distribute_cards
from gamestate import GameState

class inverseLegal(unittest.TestCase):
    def setUp(self):
        fixed_history = ["EO_", "HU_", "SU_", "E7_",
                         "EA_", "E10", "EK_", "S7_",
                         "SA_", "S10", "SK_", "G7_"]

        hand = ["GO_", "SO_", "HO_", "EU_", "GU_"]
        state = GameState(game_mode = "Herz Solo", offensive_player = 0, active=0)

        for c in fixed_history:
            state = state.result(c)
            
        self.state = state
        self.card_constraints = inverse_legal_moves(state, hand, 0)
        self.number_constraints = how_many(state, 0)
        
    def test_possible_moves(self):
        expected = {1: {'E8_', 'E9_', 'G10', 'G8_', 'G9_', 'GA_', 'GK_', 'H10',
                        'H7_', 'H8_', 'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
                    2: {'E8_', 'E9_', 'G10', 'G8_', 'G9_', 'GA_', 'GK_', 'H10',
                        'H7_', 'H8_', 'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
                    3: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'}}
                    
        self.assertEqual(self.card_constraints, expected)
        
    def test_number(self):
        expected = {1: 5, 2: 5, 3: 5}
        self.assertEqual(expected, self.number_constraints)
        
    def test_assign_hands(self):
        assignment = distribute_cards(self.card_constraints, self.number_constraints)
        for key, value in assignment.items():
            possibility = self.card_constraints[key]
            value = set(value)
            self.assertTrue(value.issubset(possibility))
        
    
if __name__ == "__main__":
    unittest.main()
