# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:44:48 2018

@author: martin
"""
from .node import Node


class SimpleNode(Node):
    """ A node which, instead of calculating all possible cards a player 
    may have, simply initializes with a set of player hands that is given to 
    it. This is used for the Perfect Information Monte Carlo bot."""
    def __init__(self, state, hands):
        self.Q = 0
        self.N = 0
        self.children = {}
        self.parent = None
        self.state = state
        self.hands = {p: set(hand) for p, hand in hands.items()}
        
        self.untried_actions = set(state.actions(self.hands[state.active]))

    def get_hand(self):
        """ This is just here so that the print_tree function has something to print."""
        return self.hands[self.state.active]
    p_hand = property(get_hand)  
    
        
    def add_child(self, action):
        new_hands = {p: set(hand) for p, hand in self.hands.items()}
        new_state = self.state.result(action)
        new_hands[self.state.active].remove(action)
        new_node = SimpleNode(new_state, new_hands)
        self.children[action] = new_node
        new_node.parent = self
        return new_node