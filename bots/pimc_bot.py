# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 13:30:29 2018

@author: martin
"""

from .heuristic_bot import HeuristicBot
from nodes import SimpleNode 
from card_counting import assign_hands
import time
import math
import random
from collections import defaultdict


class PerfectInformationMonteCarloBot(HeuristicBot):
    """ Follows a very straightfoward implementation of a perfect-information
    monte-carlo (PIMC):
    """
    def __init__(self):
        super().__init__()
        self.root_node = None
        self.player_id = None
        
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
        possible_hands = {p: set(hand) for p, hand in possible_hands.items()}
        
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
        utils = self.default_policy(new_node.state, new_node.hands)
        return new_node, utils
 

    # ----------------------------------
    def best_child(self, node, c=math.sqrt(2)):
        """ Calculates the formula for MCTS to find the child node with 
        the highest probability of winning. """    
        best_action, best_node = max(node.children.items(),
                          key=lambda x: (x[1].Q / x[1].N) 
                          + (c * math.sqrt(2 * math.log(node.N) / x[1].N)))
        return best_node, best_action
    

    
    def play_card(self, state, n_worlds = 8):
        if len(state.actions(self.hand)) == 1:
            choice = state.actions(self.hand)[0]
            self.hand.remove(choice)
            return choice

        self.player_id = state.active # is this a good idea?
        # if i ever start a simulation where another player has priority, 
        # my algorithm will assume that THAT player has MY hand. 
        
        # Initialize a search tree for each world.
        self.roots = {}
        win_probabilities = {}
        for w in range(n_worlds):
            hand_assignment = assign_hands(state, self.hand, self.player_id)
            hand_assignment[self.player_id] = set(self.hand)
            root_node = SimpleNode(state, hand_assignment)
            self.roots[w] = root_node
            win_probabilities[w] = {}
            
        # Do a Monte Carlo Tree search on each world. We alternate between worlds
        # so that a complete answer is always ready if the time runs out.
        # (Not relevant yet, but may be in the future. )
        w = 0
        count = 0
        start = time.time()
        t = time.time() - start
        depth = 0
        win_probabilities = {}
        while t < 2:
            root_node = self.roots[w]
            v, utils = self.tree_policy(root_node)
            depth = max((depth, v.depth()))
            self.back_up(v, utils)            
            win_probabilities[w] = {action: n.Q/n.N for action, n in root_node.children.items()}

            t = time.time() - start
            w = (w + 1) % n_worlds
            count += 1
        # Find the action that had the highest win ratio over all worlds. 
        average_wins = defaultdict(int)
        for world, probabilities in win_probabilities.items():
            for action, p in probabilities.items():
                average_wins[action] += p
        choice = max(average_wins.items(), key = lambda x: x[1])[0]  
        
#        print("====================")
#        print("Depth: "+str(depth))
#        print("Node Expansions: "+str(count))
        self.hand.remove(choice)
        return choice