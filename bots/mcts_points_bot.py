# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 21:34:12 2018

@author: martin
"""
from .mcts_bot import MonteCarloBot

class MonteCarloPointsBot(MonteCarloBot):
    """ Same as MonteCarloPlus, but uses the full points values for utility instead
    of {0,1}. Utilities are divided by 120 so that the utilities lie in [0,1],
    as is assumed by the UCTS monte-carlo algorithm. """
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
        
        utils = node.state.utilities(bools=False)
        utils = tuple(i*1.0/120 for i in utils)
        return node, utils  
    
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
        utils = state.utilities(bools=False)
        utils = tuple(i*1.0/120 for i in utils)
        return utils