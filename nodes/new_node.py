# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:37:30 2018

@author: martin
"""
from card_counting import distribute_cards, inverse_legal_moves, filter_playable_cards, filter_equivalent_cards, propagate_constraints
from constants import constants as con

class NewNode:
    def __init__(self, state, p_hand, p_id):
        """ must be fed with hands, which is a result from inverse_legal_moves, 
        which must have already had constraints propagated. And checked for solveability."""
        self.Q = 0
        self.N = 0
        self.children = {}
        self.parent = None
        self.state = state
        self.p_hand = set(p_hand)
        self.p_id = p_id
        self.card_constraints, self.number_constraints = inverse_legal_moves(state, p_hand, p_id)
        self.card_constraints = propagate_constraints(self.card_constraints, self.number_constraints)

        if p_id == state.active:
            self.untried_actions = set(filter_equivalent_cards(state, state.actions(self.p_hand)))
            # if we are the current active player, we can save time by ignoring
            # equivalent options
        else:
            game_mode = state.game_mode
            current_round = state.get_current_round()
            if current_round:
                card = state.get_current_round()[1:4]
                starting_suit = con.SUITS_MAPPING[state.game_mode][card]
            else:
                starting_suit = None
            player = state.active
            self.untried_actions = filter_playable_cards(self.card_constraints,
                                                         self.number_constraints,
                                                         player,
                                                         starting_suit,
                                                         game_mode)
            
    def add_child(self, action):
        new_hand = set(self.p_hand)
        new_state = self.state.result(action)
        if self.state.active == self.p_id:
            new_hand.remove(action)
        new_node = NewNode(new_state, new_hand, self.p_id)
        self.children[action] = new_node
        new_node.parent = self
        return new_node
        
    def is_fully_expanded(self):
        if self.untried_actions:
            return False
        return True
   
    def __repr__(self):
        thing = "========== Node ==========\n"
        thing += ("State: "+str(self.state.history)+"\n")
        thing += "Q: {}, N: {}\n".format(self.Q, self.N)
        thing += "Parent: {} \n".format(id(self.parent))
        thing += "Children: \n"
        for key, value in self.children.items():
            thing += "Action:{}, location: {}\n".format(key, id(value))
        return thing
    
    def print_tree(self, max_depth = 32):
        """ Prints a tree representation of the node and it's children, 
        down to a certain depth."""
        def print_util(node, prefix="", depth = 0, max_depth = 32):
            if depth == max_depth:
                return None
            printstr = ""
            for i in range(depth):
                printstr += "    "
            printstr += "|___"
            printstr += str(prefix)
            printstr += " Q: {}, N: {}, ".format(node.Q, node.N)
            printstr += "Hand: "+str(node.p_hand)+"\n"
            print(printstr)
            for key, value in node.children.items():
                print_util(value, prefix = key, depth = depth+1, max_depth = max_depth)
        print_util(self, max_depth= max_depth)
        
    def depth(self):
        def depth_util(node, count = 0):
            if node.parent is None:
                return count
            else:
                count += 1
                return depth_util(node.parent, count)
        return depth_util(self)
    
    def assign_hands(self):
        """ Generate a set of plausible hands given the play history."""
        result = distribute_cards(self.card_constraints, self.number_constraints)
        result[self.p_id] = set(self.p_hand)
        return result