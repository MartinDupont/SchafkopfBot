# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:46:12 2018

@author: martin
"""

import unittest
import random
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

class distributeCards(unittest.TestCase):
    def test_case_1(self):
        card_constraints = {0: {'EA_', 'SU_'}, 2: {'GK_', 'SU_'}, 3: {'EA_'}}
        number_constraints = {0: 1, 2: 1, 3: 1}
        assignment = distribute_cards(card_constraints, number_constraints)
        expected = {0:{"SU_"}, 2:{"GK_"}, 3:{"EA_"}}
        self.assertEqual(assignment, expected)

    def test_case_2(self):
        card_constraints = {0: {'GK_', 'G8_', 'H9_', 'H10'},
                            2: {'GK_', 'G8_', 'EA_', 'EK_'},
                            3: {'EA_', 'EK_'}}
        number_constraints = {0: 2, 2: 2, 3: 2}
        assignment = distribute_cards(card_constraints, number_constraints)
        expected = {0: {'H9_', 'H10'},
                    2: {'GK_', 'G8_'},
                    3: {'EA_', 'EK_'}}
        
        self.assertEqual(assignment, expected)



class checkCatchExceptions(unittest.TestCase):
    def test_1(self):
        """Give it an unsolveable set of constraints and see if an exception is 
        raised. This set will pass the first assertion, but not the second."""
        number_constraints = {1: 5, 2: 5, 3: 5}
        card_constraints = {1: {'E8_', 'E9_', 'H10', 'H7_', 'H8_',
                                'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
                            2: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'},
                            3: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'}}

        self.assertRaises(AssertionError,
                          distribute_cards, card_constraints, number_constraints)

        
class handAssignmentsFullGames(unittest.TestCase):
    
    def test_full_game(self):
        """ Test to see if during the course of a full game, we can correctly
        deduce which cards the other player has. I'm undecided as to whether
        we want this test to have a random element or not."""
        # Random but fixed hands. 
        hands = {0: {'SK_', 'S7_', 'H10', 'H7_', 'HK_', 'E8_', 'HU_', 'GU_'},
                 1: {'G9_', 'HO_', 'S10', 'H9_', 'EO_', 'E10', 'GO_', 'GK_'},
                 2: {'G10', 'SU_', 'G8_', 'E9_', 'G7_', 'SO_', 'S9_', 'S8_'},
                 3: {'GA_', 'EU_', 'E7_', 'H8_', 'SA_', 'EA_', 'EK_', 'HA_'}}
        
        state = GameState(game_mode = "Herz Solo", offensive_player = 1, active=0)
        
        for _ in range(32):   
            active = state.active
            action = random.choice(state.actions(hands[active]))
            hands[active].remove(action)
            state = state.result(action)
            
            for i in range(4):
                card_constraints = inverse_legal_moves(state, hands[i], i)
                for p_num, card_set in card_constraints.items():
                    actual_hand = hands[p_num]
                    self.assertTrue(actual_hand.issubset(card_set))
                    # after each play, check that the card constraints for each
                    # active players perspective can possbly contain the opponents current_hand. 
        
    
    
    
if __name__ == "__main__":    
    unittest.main()
