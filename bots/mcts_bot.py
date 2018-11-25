# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:31:45 2018

@author: martin
"""

from .heuristic_bot import HeuristicBot
from nodes import Node
import time
import math
import random


class MonteCarloBot(HeuristicBot):
    """ Follows a modified implementation of a Monte Carlo Tree Search:
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    
    The algorithm had to be modified slightly, because schafkopf is an incomplete
    information game. With this algorithm, opponents can play any of the cards that have not been 
    played so far, and that are not known to be in this players hand, which
    do not lead to impossible situations, such as players having played illegally. 
    (Except for davonlaufen, that's not implemented yet).
    """
    def __init__(self, c = math.sqrt(2)):
        super().__init__()
        self.root_node = None
        self.player_id = None
        self.c = c
        
#    def play_or_not(self, i):
#        return False
    
    # -------------------------  
    def tree_policy(self, node):
        """ If the node has not been fully expanded, we add a child node
        and run the default policy on it, delivering a node and utilities. 
        Sometimes, the node may actually not be expandable, and we raise an error"""
        while not node.state.terminal_test():
            if not node.is_fully_expanded():
                try:
                    return self.expand_node(node)
                except AssertionError:
                    continue
            else:
                node, _ = self.best_child(node)
        return node, node.state.utilities()  
    
    def default_policy(self, state, possible_hands):
        """ Given some consistent assignment of hands, each player then 
        plays randomly until the end of the game.
        
        Returns
        -------
        utils: tuple of length 4. 
        """
        while not state.terminal_test():
            active = state.active
            active_hand = possible_hands[active]
            action = random.choice(state.actions(active_hand))
            active_hand.remove(action)
            state = state.result(action)
        return state.utilities()
    
    def back_up(self, node, utils):
        """Backup function is unchanged from standard MCTS implementation."""
        while not(node.parent is None):
            p_num = node.parent.state.active
            node.N += 1
            node.Q += utils[p_num]
            node = node.parent  
        node.N += 1
            
    def expand_node(self, input_node):
        action = input_node.untried_actions.pop()
        new_node = input_node.add_child(action) 
        # will raise an exception if a is not valid
        hand_assignment = new_node.assign_hands()
        utils = self.default_policy(new_node.state, hand_assignment)
        return new_node, utils
 

    # ----------------------------------
    def best_child(self, node, c=None):
        """ Calculates the formula for MCTS to find the child node with 
        the highest probability of winning. """ 
        
        if c == None:
            c = self.c
        best_action, best_node = max(node.children.items(),
                          key=lambda x: (x[1].Q / x[1].N) 
                          + (c * math.sqrt(2 * math.log(node.N) / x[1].N)))
        return best_node, best_action
    

    
    def play_card(self, state):
        if len(state.actions(self.hand)) == 1:
            choice = state.actions(self.hand)[0]
            self.hand.remove(choice)
            return choice

        self.player_id = state.active # is this a good idea?
        self.root_node = Node(state, set(self.hand), self.player_id)
        # if i ever start a simulation where another player has priority, 
        # my algorithm will assume that THAT player has MY hand. 
        i=0
        start = time.time()
        t = time.time() - start
        depth = 0
        while t < 2:
            v, utils = self.tree_policy(self.root_node)
            depth = max((depth, v.depth()))
            self.back_up(v, utils)
            node, action = self.best_child(self.root_node, 0)
            choice = action
            t = time.time() - start
            i+=1
#        print("====================")
#        print("Depth: "+str(depth))
#        print("N cycles: "+str(i))
        self.hand.remove(choice)
        return choice