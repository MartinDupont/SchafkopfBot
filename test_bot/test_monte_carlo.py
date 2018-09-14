# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 16:02:47 2018

@author: martin
"""

import unittest

from bots import MonteCarloBot
from nodes import Node
from gamestate import GameState


class TestNodes(unittest.TestCase):
    def setUp(self):
        state = GameState(game_mode = "Herz Solo", offensive_player = 1, active=0)
        p_hand = ['EK_', 'EU_', 'G10', 'SA_', 'HK_', 'H7_', 'S7_', 'H10']
        p_id = 0
        self.node = Node(state, p_hand, p_id)
        self.node.add_child("EK_")
       
    def test_hand(self):
        result = self.node.children["EK_"].p_hand
        expected = set(['EU_', 'G10', 'SA_', 'HK_', 'H7_', 'S7_', 'H10'])
        self.assertEqual(result, expected)


class Check_MCTS(unittest.TestCase):
    """ Really gotta expand this"""
    def setUp(self):
        self.bot = MonteCarloBot()
        self.bot.hand = ['G7_', 'HO_', 'EO_', 'GU_', 'HU_', 'SA_', 'GK_', 'EK_']
        game_mode = "Herz Solo"
        self.state = GameState(game_mode = game_mode, offensive_player = 0, active=0)
        
    def test_play(self):
        """ Check that he can play a single card without error."""
        state = self.state.result("E10")
        action = self.bot.play_card(state)
        expected = "EK_"
        self.assertEqual(action, expected)        

class TestMonteCarlo(unittest.TestCase):
    def setUp(self):
        self.bot = MonteCarloBot()
        
    def test_tree(self):
        """ Test a case where the optimal move is known, and the search tree
        is small enough to be checked manually."""
        state = GameState(game_mode = "Herz Solo", offensive_player = 0, active=0)
        
        fixed_history = ["SO_", "EO_", "HO_", "GO_", # 0 starts and 1 wins 12 pts
                         "SU_", "GU_", "HU_", "EU_", # 1 starts and 0 wins 8pts
                         "H10", "HA_", "HK_", "H9_", # 0 starts and 1 wins 25 pts
                         "E9_", "E10", "EK_", "EA_", # 1 starts and 0 wins 25 pts
                         "GA_", "G10", "GK_", "G9_", # 0 starts and 0 win 25 points
                         "S7_", "SA_", "SK_", "S9_", # 0 starts and 1 wins 15 pts
                         "E8_", "S10", "H7_"]         # 1 starts ...
        # 3 has 52 pts, 0 has 58 pts, and is the active player.                
        # This is now the deciding move. 0 must play the H8_ if he wants to win.  

        #remaining  = ["H8_", "G8_", "G7_", "S8_", "E7_"]
        for action in fixed_history:
            state = state.result(action)

        hand = {"H8_", "G7_"}
        
        root_node = Node(state, set(hand), 0) 
        # just running the main loop in play_card() manually, to check that 
        # the tree is correctly structured.
        for _ in range(100):
            v, utils = self.bot.tree_policy(root_node)
            self.bot.back_up(v, utils)
            node, action = self.bot.best_child(root_node, 0)
            choice = action

        self.assertEqual(choice, "H8_")
        # There is one and only one winning move, the H8_.
         
        path = ["H8_", "G7_", "E7_"]
        winning_path_1 = path + ["S8_", "G8_"]
        winning_path_2 = path + ["G8_", "S8_"]
        # and only two possible ways to get there. 
        
        node_1 = root_node
        node_2 = root_node
        for p_1, p_2 in zip(winning_path_1, winning_path_2):
            node_1 = node_1.children[p_1]
            node_2 = node_2.children[p_2]
            
        # Checking that the tree structure is correct. Due to Randomness of 
        # MCTS, the bot will not explore the whole final game tree, just the
        # most promising branches. 
        self.assertTrue(node_1.state.terminal_test())
        self.assertEqual(node_1.state.utilities(), (1, 0, 0, 0))
        
        self.assertTrue(node_2.state.terminal_test())
        self.assertEqual(node_2.state.utilities(), (1, 0, 0, 0))
        
        self.assertEqual(set(root_node.children.keys()), hand)
        
        
                           
    #=========================================================================#                        
    #                              Game Tree
    #=========================================================================#
    # key: |P:2| is a node where player 2 chooses.
    #
    #                                                      |P:3| -- S8 -- |END|
    #                                                     / 
    #                                                   G8  
    #                                                  /    
    #               |P:0| -- G7 -- |P:1| -- E7 -- |P:2|               
    #              /                                   \    
    #             /                                     S8       
    #           H8                                        \   
    #          /                                           |P:3| -- G8 -- |END| 
    #         /                                         
    #|Root P:0|                               
    #         \                                    
    #          \             |P:0| -- H8 -- |P:1| -- E7 -- |P:2| -- S8 -- |END|  
    #           G7          /          
    #             \       G8           
    #              \     /             
    #               |P:3|              
    #                    \             
    #                     S8          
    #                       \         
    #                        |P:0| -- H8 -- |P:1| -- E7 -- |P:2| -- G8 -- |END|
    #=========================================================================#

#
#    
#    def test_1(self):
#        pass
#    
#    
#    
#            hands = {0: ['SK_', 'S9_', 'EO_', 'H8_', 'SO_', 'EU_', 'E7_', 'E8_'],
#                 1: ['GK_', 'HA_', 'SU_', 'G8_', 'G10', 'EK_', 'HK_', 'GU_'],
#                 2: ['S7_', 'S10', 'E9_', 'GA_', 'H10', 'H7_', 'HU_', 'E10'],
#                 3: ['S8_', 'G9_', 'H9_', 'G7_', 'SA_', 'GO_', 'HO_', 'EA_']}