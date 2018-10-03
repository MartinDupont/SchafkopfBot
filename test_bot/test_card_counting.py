# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:46:12 2018

@author: martin
"""

import unittest
import random
from card_counting import inverse_legal_moves, assign_hands, distribute_cards, propagate_constraints, filter_equivalent_cards
from gamestate import GameState

class inverseLegal(unittest.TestCase):
    """ Check that the function can correctly detect which cards cannot belong 
    to certain players, and how many cards each player needs to be assigned. """
    def setUp(self):
        fixed_history = ["EO_", "HU_", "SU_", "E7_",
                         "EA_", "E10", "EK_", "S7_",
                         "SA_", "S10", "SK_", "G7_"]

        hand = ["GO_", "SO_", "HO_", "EU_", "GU_"]
        state = GameState(game_mode = "Herz Solo", offensive_player = 0, active=0)

        for c in fixed_history:
            state = state.result(c)
            
        self.state = state
        self.card_constraints, self.number_constraints = inverse_legal_moves(state, hand, 0)
        #self.number_constraints = how_many(state, 0)
        
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

class constraintPropagation(unittest.TestCase):
    """ Check that my constraint propagation is working. Given a list of 
    cards that the players may have, we can cross of certain possibilities."""
    def test_1(self):
        card_constraints = {0: {'SK_', 'S8_', 'H9_', 'H10'},
                            2: {'SK_', 'S8_', 'EA_', 'EK_'},
                            3: {'EA_', 'EK_'}}
        number_constraints = {0: 2, 2: 2, 3: 2}
        result = propagate_constraints(card_constraints, number_constraints)
        expected = {0: {'H9_', 'H10'},
                    2: {'SK_', 'S8_'},
                    3: {'EA_', 'EK_'}}
        self.assertEqual(result, expected)


class distributeCards(unittest.TestCase):
    """ We construct some cases in which there is only one possible assignment
    of cards. """
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
        
    def test_case_3(self):
        """ Test that it can solve a case with multiple solutions """
        card_constraints = {1: {'E8_', 'E9_', 'G10', 'G8_', 'G9_', 'GA_', 'GK_', 'H10',
                            'H7_', 'H8_', 'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
               2: {'E8_', 'E9_', 'G10', 'G8_', 'G9_', 'GA_', 'GK_', 'H10',
                            'H7_', 'H8_', 'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
               3: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'}}        
            
        number_constraints = {1: 5, 2: 5, 3: 5} 
         
        result = distribute_cards(card_constraints, number_constraints) 
        for i in card_constraints.keys():
            self.assertTrue(result[i].issubset(card_constraints[i]))


class checkCatchExceptions(unittest.TestCase):
    def test_1(self):
        """Give it an unsolveable set of constraints and see if an exception is 
        raised. This set will pass the first assertion, but not the second."""
        number_constraints = {1: 5, 2: 5, 3: 5}
        card_constraints = {1: {'E8_', 'E9_', 'H10', 'H7_', 'H8_',
                                'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
                            2: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'},
                            3: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'}}

        self.assertRaises(ValueError,
                          distribute_cards, card_constraints, number_constraints)
        
    def test_2(self): 
        """ Test for a second-order unsolveability. Each of 2 or 3 alone could
        be given 4 cards matching their constraints, but the two of them 
        together cannot, becuase the union of their allowed_cards has len < 4+4.
        """
        number_constraints = {2: 4, 3: 4, 0: 5}
        
        card_constraints = {2: {'G7_', 'E10', 'E8_', 'HK_', 'G9_'},
                            3: {'G7_', 'E10', 'E8_', 'HK_', 'G9_'},
                            0: {'SU_', 'G7_', 'GU_', 'S9_', 'E10', 
                                'S10', 'HO_', 'GO_', 'E8_', 'HK_',
                                'S8_', 'S7_', 'G9_'}}
        self.assertRaises(ValueError,
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
                card_constraints, _ = inverse_legal_moves(state, hands[i], i)
                for p_num, card_set in card_constraints.items():
                    actual_hand = hands[p_num]
                    self.assertTrue(actual_hand.issubset(card_set))
                    # after each play, check that the card constraints for each
                    # active players perspective can possbly contain the opponents current_hand. 
                    
                    
    def test_full_game_2(self):
            """ Test to see if during the course of a full game, we can correctly
            assign cards to players without raising any exceptions. I'm
            undecided as to whether we want this test to have a random element
            or not."""
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
                    arbitrary_assignment = assign_hands(state, hands[i],i )
                    # try and assign some hands. If he can't find a solution, it will raise an exception. 
        
class CheckFilterEquivalentCards(unittest.TestCase):
    def setUp(self):
        self.state_1 = GameState(game_mode = "Partner Eichel", offensive_player = 1, active=0)
        self.state_2 = GameState(game_mode = "Wenz", offensive_player = 1, active=0)
        self.fixed_history_1 = ["E7_", "E8_", "E9_", "GO_", "H8_"]
        self.fixed_history_2 = ["EA_", "E10", "E8_", "HU_", "EU_"]
        #self.fixed_history_3 = ["E8", "E10", "EK_", "EA_"]
    
    def test_equivalent_obers(self):
        state = self.state_1

        for card in self.fixed_history_1:
            state = state.result(card)
        
        result = filter_equivalent_cards(state, ["HO_", "EO_"])
        expected = ["HO_"]
        self.assertEqual(result, expected)
        
    def test_ignore_current_round(self):
        """ If someone else has played a card between two of my cards, in 
        the current round, then my cards cannot be considered equivalent. """
        state = self.state_1

        for card in self.fixed_history_1:
            state = state.result(card)
        
        result = filter_equivalent_cards(state, ["H7_", "H9_"])
        expected = ["H7_", "H9_"]
        self.assertEqual(result, expected)
        

    def test_equivalent_unters(self):
        state = self.state_1
        for card in self.fixed_history_2:
            state = state.result(card)
            
        result = filter_equivalent_cards(state, ["SU_", "GU_", "E7_", "S7_", "G7_"])
        expected = ["SU_", "E7_", "S7_", "G7_"]
        self.assertEqual(set(result), set(expected))
        
    def test_equivalent_spatzen(self):
        state = self.state_1
        for card in self.fixed_history_2:
            state = state.result(card)
            
        result = filter_equivalent_cards(state, ["E7_", "E9_", "EK_"])
        expected = ["E7_", "EK_"]
        self.assertEqual(set(result), set(expected))
        
    def test_wenz_ignore_obers(self):
        """ Obers are not trumps in a wenz. """
        state = self.state_2
        for card in self.fixed_history_1:
            state = state.result(card)
        
        result = filter_equivalent_cards(state, ["SO_", "HO_", "EO_"])
        expected = ["SO_", "HO_", "EO_"]
        self.assertEqual(set(result), set(expected))
        
    
if __name__ == "__main__":    
    unittest.main()
