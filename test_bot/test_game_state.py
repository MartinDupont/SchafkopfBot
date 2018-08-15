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
        self.state = GameState(game_mode = self.gamemode, offensive_player = 1, active=0)
    
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
        
    def test_last_card(self):
        new_state = self.state.result("G10")
        new_hand = ["EA"]
        allowed = new_state.actions(new_hand)
        expected = new_hand
        self.assertEqual(allowed, expected)
        

        

class CheckWenz(unittest.TestCase):
    def setUp(self):
        self.gamemode = "Wenz"
        self.hand = ["E7_", "EA_", "HU_" ,"EU_", "SU_"]
        self.state = GameState(game_mode = self.gamemode, offensive_player = 0, active=0)  
        
    def test_follow_unter(self):
        new_state = self.state.result("GU_")
        allowed = new_state.actions(self.hand)
        expected = ["HU_", "EU_", "SU_"]
        self.assertEqual(allowed, expected)
        
    def test_follow_normal(self):
        new_state = self.state.result("E10")
        allowed = new_state.actions(self.hand)
        expected = ["E7_", "EA_"]
        self.assertEqual(allowed, expected)
        
    def test_free(self):
        new_state = self.state.result("HK_")
        allowed = new_state.actions(self.hand)
        expected = self.hand
        self.assertEqual(allowed, expected)
        
    def test_obers_not_trumps(self):
        state = self.state.result("EU_")
        state = state.result("HU_")
        state = state.result("SU_")
        state = state.result("EO_")
        winner, points = state.calculate_round_winner(state.history)
        self.assertEqual(0, winner)
        self.assertEqual(9, points)
        
    def test_utilities(self):
        """ Doing a Wenz in which the first guy doesn't lose a single hand."""
        fixed_history = ["EU_", "GU_", "HU_", "E7_",
                         "SU_", "S7_", "G7_", "H7_",
                         "EA_", "E10", "EK_", "E9_",
                         "SA_", "S10", "SK_", "S9_",
                         "HA_", "H7_", "H8_", "H9_"]
        total_points = 6 + 2 + 25 + 25 + 11
        
        state = self.state
        for card in fixed_history:
            state = state.result(card)
            
        self.assertTrue(state.is_decided())
        self.assertEqual((1, 0, 0, 0), state.utilities(intermediate=True))
        self.assertEqual((total_points, 0, 0, 0),
                         state.utilities(bools=False, intermediate=True))
        
class CheckRoundPoints(unittest.TestCase):
    def setUp(self):
        self.state = GameState(game_mode = "Herz Solo", offensive_player = 0, active=0)
    
    def test_trump_open(self):
        state = self.state.result("EO_")
        state = state.result("HA_")
        state = state.result("E10")
        state = state.result("S8_")
        winner, points = state.calculate_round_winner(state.history)
        self.assertEqual(0, winner)
        self.assertEqual(3+11+10, points)
        
    def normal_open_trumped(self):
        state = self.state.result("S8_")
        state = state.result("S10_")
        state = state.result("HU_")
        state = state.result("SO_")
        winner, points = state.calculate_round_winner(state.history)
        self.assertEqual(3, winner)
        self.assertEqual(15, points)
        
    def normal_open(self):
        state = self.state.result("E9_")
        state = state.result("E10")
        state = state.result("E8_")
        state = state.result("EA_")
        winner, points = state.calculate_round_winner(state.history)
        self.assertEqual(3, winner)
        self.assertEqual(21, points)
        
    def test_winner_calculations(self):
        """ Do a Solo in which the first guy definitely wins."""
        fixed_history = ["EO_", "GO_", "HO_", "SO_",
                         "EU_", "GU_", "HU_", "SU_",
                         "HA_", "H10", "HK_", "H9_",
                         "EA_", "E10", "EK_", "E9_",
                         "GA_", "G10", "GK_", "G9_",
                         "SA_", "S10", "SK_", "S9_",
                         "H8_", "E8_", "E7_", "G8_",
                         "H7_", "G7_", "S8_", "S7_"]
        
        state = self.state
        for card in fixed_history:
            state = state.result(card)
        
        utility = state.utilities()
        expected = (1, 0, 0, 0)
        self.assertEqual(utility, expected)
        
        
    def test_winner_utils(self):
        """" Fixed history for a hame in which palyers 1 and 2 win, but player
        3 called the ace, and player 0 had it."""
        state = GameState(game_mode = "Partner Gras", offensive_player = 3, active=3)
        
        fixed_history=  ["S8_", "SA_", "S10", "S9_",    # Player 0 wins 21 points
                         "GU_", "HO_", "HU_", "H10",    # player 1 wins 17 points
                         "EK_", "E8_", "EA_", "E10",    # player 3 wins 25 points
                         "SO_", "H7_", "E7_", "HK_",    # player 3 wins 7 points
                         "EU_", "H8_", "G8_", "EO_",    # player 2 wins 5 points
                         "SU_", "H9_", "G9_", "G7_",    # player 2 wins 2 points
                         "GO_", "E9_", "SK_", "G10",    # player 2 wins 17 points
                         "HA_", "S7_", "GA_", "GK_"]    # player 2 wins 26 points
        
        for action in fixed_history:
            state = state.result(action)
        
        utils = state.utilities()
        expected = (0, 1, 1, 0)
        self.assertEqual(utils, expected)
        
        points_tally = state.tally_points()
        expected = (53, 67, 67, 53)
        self.assertEqual(points_tally, expected)
        
class CheckRamsch(unittest.TestCase):
    def setUp(self):
        self.state = GameState(game_mode = "Ramsch", offensive_player = None, active=0)
        
    def test_winner_calculations(self):
        """ Do a Ramsch in which the first guy definitely loses."""
        fixed_history = ["EO_", "GO_", "HO_", "SO_",
                         "EU_", "GU_", "HU_", "SU_",
                         "HA_", "H10", "HK_", "H9_",
                         "EA_", "E10", "EK_", "E9_",
                         "GA_", "G10", "GK_", "G9_",
                         "SA_", "S10", "SK_", "S9_",
                         "H8_", "E8_", "E7_", "G8_",
                         "H7_", "G7_", "S8_", "S7_"]
        state = self.state
        for i, card in enumerate(fixed_history):
            state = state.result(card)
                
        utility = state.utilities()
        expected = (0, 1, 1, 1)
        self.assertEqual(utility, expected)
        
    def test_partial_utilities(self):
        """ Test that the utilities are calculated correctly before and
        after the game is decided."""
        fixed_history = ["EO_", "GO_", "HO_", "SO_",
                         "EU_", "GU_", "HU_", "SU_",
                         "HA_", "H10", "HK_", "H9_",
                         "EA_", "E10", "EK_", "E9_"]
        state = self.state
        for i, card in enumerate(fixed_history):
            state = state.result(card)
            if i == 12:
                decided = state.is_decided()
                self.assertTrue(not decided)
                bool_utils = state.utilities(intermediate= True)
                self.assertEqual((0,0,0,0), bool_utils)
                point_utils = state.utilities(bools=False, intermediate=True)
                self.assertEqual((75, 120, 120, 120), point_utils)
                
        decided = state.is_decided()
        self.assertTrue(decided)
        bool_utils = state.utilities(intermediate = True)
        self.assertEqual((0,1,1,1), bool_utils)
                
                

class CheckIsDecided(unittest.TestCase):
    def check_solo(self):
        """ Do a Solo in which the first guy definitely wins before the game is over."""
        state = GameState(game_mode = "Herz Solo", offensive_player = 0, active=0)
        fixed_history = ["EO_", "GO_", "HO_", "SO_",
                         "EU_", "GU_", "HU_", "SU_",
                         "HA_", "H10", "HK_", "H9_"]
        
        for card in fixed_history:
            state = state.result(card)
        
        self.assertTrue(not state.is_decided())
        
        extra_history = ["EA_", "E10", "EK_", "E9_"]
        for card in extra_history:
            state = state.result(card)
        
        self.assertTrue(state.is_decided())
        
    def check_ramsch(self):
        """Do a ramsch in which the first guy has lost before the game is over."""
        state = GameState(game_mode = "Ramsch", offensive_player = 0, active=0)
        fixed_history = ["EO_", "GO_", "HO_", "SO_",
                         "EU_", "GU_", "HU_", "SU_",
                         "HA_", "H10", "HK_", "H9_"]
        
        for card in fixed_history:
            state = state.result(card)
        
        self.assertTrue(not state.is_decided())
        extra_history = ["EA_", "E10", "EK_", "E9_"]
        for card in extra_history:
            state = state.result(card)
            
        self.assertTrue(state.is_decided())
        
    def check_partner(self):
        state = GameState(game_mode = "Partner Eichel", offensive_player = 0, active=0)
        fixed_history = ["E7_", "E10",  "EK_", "EA_", #player 0 starts, player 3 wins 25 pts
                         "EO_", "HA_", "H10_", "HK_",  # player 3 opens, player 3 wins 28 pts
                         "SA_", "S10", "SK_", "S9_"] # player 3 opens, player 3 wins 25 pts.

        for card in fixed_history:
            state = state.result(card)
        self.assertTrue(state.is_decided())
        
        utilities = state.utilities(bools=False, intermediate=True)
        expected = (78, 0, 0, 78)
        self.assertEqual(expected, utilities)
        
    def check_unknown_partner(self):
        state = GameState(game_mode = "Partner Eichel", offensive_player = 0, active=0)
        fixed_history = ["EO_", "HA_", "H10_", "HK_",
                         "SA_", "S10", "SK_", "S9_",
                         "E7_", "E8_",  "E9_"]

        for card in fixed_history:
            state = state.result(card)
            
        self.assertTrue(not state.is_decided())
        utilities = state.utilities(bools=False, intermediate=True)
        expected = (53, 0, 0, 0)
        self.assertEqual(utilities, expected)
        
        state = state.result("EA_")
        
        self.assertTrue(state.is_decided())
        utilities = state.utilities(bools=False, intermediate=True)
        expected = (64, 0, 0, 64)
        self.assertEqual(utilities, expected)
        
      
class CheckFullGame(unittest.TestCase):
    
    def test_full_game(self):
        """ Test that I can run a game all the way to the end without an error."""
        # Random, but fixed, opening hands. 
        hand_0 = ['EA_', 'EO_', 'S10', 'G8_', 'S7_', 'SA_', 'GU_', 'E7_']
        hand_1 = ['S8_', 'E10', 'SU_', 'GA_', 'HO_', 'H9_', 'H7_', 'SO_']
        hand_2 = ['EU_', 'H8_', 'SK_', 'G7_', 'G9_', 'EK_', 'HU_', 'GO_']
        hand_3 = ['HK_', 'HA_', 'GK_', 'H10', 'E9_', 'G10', 'E8_', 'S9_']  
        player_dict = {0:hand_0, 1:hand_1, 2:hand_2, 3:hand_3}
        
        # Player 1 calls a eichel partner play, (with player 0.)
        state = GameState(game_mode="Partner Eichel", offensive_player=1, active=0)
        for i in range(8):
            for j in range(4):
                hand = player_dict[state.active]
                possible = state.actions(hand)
                chosen = possible[0] 
                # pick the first of the possible moves, don't want randomness in unittests.
                state = state.result(chosen)
                hand.remove(chosen)
            state.calculate_round_winner(state.history[-16:])
            state.utilities()
        self.assertTrue(state.terminal_test())
        self.assertEqual(state.played_the_ace(), 0) # correctly identifies who the partner is.
 
#class CheckPrinting(unittest.TestCase)
#    hist = '0EA_1E102EK_3E9_0EO_1SU_2EU_3HK_0S101S8_2SK_3S9_0G8_1GA_2G7_3GK_1HO_2H8_3HA_0GU_1H9_2HU_3H100S7_2G9_3G100SA_1H7_1SO_2GO_3E8_0E7_'

      
if __name__ == "__main__":
    unittest.main()