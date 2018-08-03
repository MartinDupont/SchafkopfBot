# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:46:15 2018

@author: martin
"""
import constants as con
from bots import DumbBot, unplayed_cards
from distribute_cards import distribute_cards
import copy
import time
import math
import random


def inverse_legal_moves(state, hand, p_id):
    """ Given the history of the game so far, and the hand of the player
    calling the function, for each player we find a set of cards that have not
    been ruled out by the history. 
    
    This only considers when a player played a card of the wrong suit.
    This means that in a partner game, when a player "runs away", this function
    will not be able to detect who has the ace. 

    Returns
    -------
    dict of sets.
    """
    hand = set(hand)
    other_players = [(i + p_id) % 4 for i in range(1, 4)]
    starting_set = set(con.ALL_CARDS) - hand
    players_may_have = {p : copy.deepcopy(starting_set) for p in other_players}
    suits_mapping = con.SUITS_MAPPING[state.game_mode]
    # All other players start with all possible cards that are not in our hand.
    for round_str in state.split_by_stride(state.history, stride = 16):
        starting_suit = suits_mapping[round_str[1:4]]
        for p, card in state.player_card_tuples(round_str):
            for p_num in other_players:
                players_may_have[p_num].discard(card)
                
            suit = suits_mapping[card]
            if (suit != starting_suit) and (p != p_id):
                temp = {c for c in players_may_have[p] if  suits_mapping[c] != starting_suit}                
                players_may_have[p] = temp

    return players_may_have

def how_many(state, p_id):
    """ Determines how many cards each player should have in their hand.
    Returns
    -------
    dict
        A dict mapping player number to number of required cards. 
    """
    other_players = [(i + p_id) % 4 for i in range(1, 4)]
    counts = {p:8 for p in other_players}
    for p, card in state.player_card_tuples(state.history):
        if p != p_id:
            counts[p] -= 1
        
    return counts
    
def assign_hands(state, p_hand, p_id):
    """ Returns a dict of possible hands for a player given that we know
    the hand of player p_id. Returns only A plausible solution. """
    number_constraints = how_many(state, p_id)
    card_constraints = inverse_legal_moves(state, p_hand, p_id)
    result = distribute_cards(card_constraints, number_constraints)
    return result

class Node:
    def __init__(self, state, p_hand, p_id):
        self.Q = 0
        self.N = 0
        self.children = {}
        self.parent = None
        self.state = state
        self.p_hand = set(p_hand)
        self.p_id = p_id
        if p_id == state.active:
            self.untried_actions = set(iter(state.actions(p_hand)))
        else:
            card_constraints = inverse_legal_moves(state, p_hand, p_id)
            self.untried_actions = card_constraints[state.active]
            
    def add_child(self, action):
        new_hand = copy.deepcopy(self.p_hand)
        if self.state.active == self.p_id:
            new_hand.remove(action)
        new_state = self.state.result(action)
        new_node = Node(new_state, new_hand, self.p_id)
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
    
    def print_tree(self):
        def print_util(node, prefix="", depth = 0):
            printstr = ""
            for i in range(depth):
                printstr += "     "
            printstr += "|___"
            printstr += str(prefix)
            printstr += " Q: {}, N: {}, ".format(node.Q, node.N)
            printstr += "Hand: "+str(node.p_hand)+"\n"
            print(printstr)
            for key, value in node.children.items():
                print_util(value, prefix = key, depth = depth+1)
        print_util(self)
        
    def depth(self):
        def depth_util(node, count = 0):
            if node.parent is None:
                return count
            else:
                count += 1
                return depth_util(node.parent, count)
        return depth_util(self)


class MonteCarloPlus(DumbBot):
    """ Follows a very straightfoward implementation of a Monte Carlo Tree Search:
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    
    The algorithm had to be modified slightly, because schafkopf is an incomplete
    information game. Opponents can play any of the cards that have not been 
    played so far, and that are not known to be in this players hand, which
    do not lead to impossible situations, such as players having played illegally. 
    (Except for davonlaufen).
    """
    def __init__(self):
        super().__init__()
        self.root_node = None
        self.player_id = None
        
    def play_or_not(self):
        return False
    
    # -------------------------  
    def tree_policy(self, node):
        """ If the node has not been fully expanded, we add a child node
        and run the default policy on it, delivering a node and utilities. 
        Sometimes, the node may actually not be expandable, and we raise an error"""
        while not node.state.terminal_test():
            if not node.is_fully_expanded():
                tup = self.expand_node(node)
                if not (tup == (None, None)):
                    return tup
                else:
                    continue
            else:
                node, _ = self.best_child(node)
        return node , node.state.utilities()  
    
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
            #print(active_hand)
            action = random.choice(state.actions(active_hand))
            active_hand.remove(action)
            state = state.result(action)
        return state.utilities()
    
    def back_up(self, node, utils):
        """back_up function is unchanged from standard implementation"""
        while not(node.parent is None):
            p_num = node.parent.state.active
            node.N += 1
            node.Q += utils[p_num]
            node = node.parent  
        node.N += 1
            
    def expand_node(self, input_node):
        a = input_node.untried_actions.pop()
        try:
            new_node = input_node.add_child(a)
            possible_hands = assign_hands(new_node.state, new_node.p_hand, new_node.p_id)
            possible_hands[new_node.p_id] = copy.deepcopy(new_node.p_hand)
            utils = self.default_policy(new_node.state, possible_hands)
            return new_node, utils
        except AssertionError:
            #print(how_many(input_node.state, input_node.p_id))
            #print(inverse_legal_moves(input_node.state, input_node.p_hand, input_node.p_id))
            del input_node.children[a]
            return None, None

    # ----------------------------------
    def best_child(self, node, c=math.sqrt(2)):
        """ has been checked, is delivering the best children, given the inputs"""    
        best_action, best_node = max(node.children.items(),
                          key=lambda x: (x[1].Q / x[1].N) 
                          + (c * math.sqrt(2 * math.log(node.N) / x[1].N)))
        return best_node, best_action
    

    
    def play_card(self, state):
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
            depth = max((depth,v.depth()))
            self.back_up(v, utils)
            node, action = self.best_child(self.root_node, 0)
            choice = action
            t = time.time() - start
            i+=1

        print("Depth: "+str(depth))
        print("N cycles: "+str(i))
        self.hand.remove(choice)
        return choice