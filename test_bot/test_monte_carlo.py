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
        
    def test_back_up(self):
        """ back_up should propagate some utilities back up the tree.
        Each nodes Q value should be incremented by the utility of the active
        player. Except the root node, which has Q = 0, as the best_child
        function is never called on the root node. """
        root_node = Node(self.state, self.bot.hand, 0)
        node = root_node
        for card in ["EK_", "E9_", "E8_", "EA_"]:
            node.add_child(card)
            node = node.children[card]

        utils = (1, -1, -0.5, 0.5)
        # fractional utilities may never be realized, but they allow us to 
        # tell that the correct utils have been assigned.
        self.bot.back_up(node, utils)
        i = 3
        while not (node.parent is None):
            self.assertEqual(node.N, 1)
            self.assertEqual(node.Q, utils[i])
            i -= 1
            node = node.parent
        self.assertEqual(node.N, 1)
    
    def test_default_policy(self):
        """ default_policy just plays random games given a hand assigment, 
        so we just need to check that it can run to the end and deliver
        a utility score. """
        hand_0 = ['EA_', 'EO_', 'S10', 'G8_', 'S7_', 'SA_', 'GU_', 'E7_']
        hand_1 = ['S8_', 'E10', 'SU_', 'GA_', 'HO_', 'H9_', 'H7_', 'SO_']
        hand_2 = ['EU_', 'H8_', 'SK_', 'G7_', 'G9_', 'EK_', 'HU_', 'GO_']
        hand_3 = ['HK_', 'HA_', 'GK_', 'H10', 'E9_', 'G10', 'E8_', 'S9_']  
        player_dict = {0:hand_0, 1:hand_1, 2:hand_2, 3:hand_3}
        # random but fixed hands
        result = self.bot.default_policy(self.state, player_dict)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)
        
    def test_expand_node(self):
        """ it should add a child to the node, with the correct actions."""
        root_node = Node(self.state, self.bot.hand, 0)
        node, _ = self.bot.expand_node(root_node)
        
        action = list(root_node.children.keys())[0]
        self.assertTrue(action in self.bot.hand)
        
    def test_best_child(self):
        """ it should pick the child with the highest probability of winning."""
        root_node = Node(self.state, self.bot.hand, 0)
        q_vals = (5, 0, 0)
        for i in range(3):
            node, _ = self.bot.expand_node(root_node)
            node.N = 5
            node.Q = q_vals[i]
        
        root_node.N = 15
        best, _ = self.bot.best_child(root_node)
        self.assertEqual(best.Q, 5)
        
    
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
