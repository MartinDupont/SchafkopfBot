# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 17:30:36 2018

@author: martin
"""
import constants as con
import copy
from distribute_cards import distribute_cards, propagate_constraints, check_solveable


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
    card_constraints = {p: set(starting_set) for p in other_players}
    number_constraints = {p :8 for p in other_players}

    suits_mapping = con.SUITS_MAPPING[state.game_mode]
    # All other players start with all possible cards that are not in our hand.
    count = 0
    for p, card in state.player_card_tuples(state.history):
        if count == 0:
            starting_suit = suits_mapping[card]
            
        for p_2 in other_players:
            card_constraints[p_2].discard(card)
            
        if p != p_id:
            number_constraints[p] -= 1    
            suit = suits_mapping[card]
            if (suit != starting_suit) and (p != p_id):
                temp = {c for c in card_constraints[p] if  suits_mapping[c] != starting_suit}                
                card_constraints[p] = temp
    
        count = (count + 1) % 4     

    return card_constraints, number_constraints


def increment_legal_moves(state, card, players_may_have):
    active = state.active
    players_may_have = copy.deepcopy(players_may_have)
    suits_mapping = con.SUITS_MAPPING[state.game_mode]
    n_played = len(state.history)
    
    for value in players_may_have.values():
        value.discard(card)
    if n_played %16 != 0:
        round_str = state.history[-n_played:]
        starting_suit = suits_mapping[round_str[1:4]]
        played_suit = suits_mapping[card]
        if played_suit != starting_suit:
            temp = {c for c in players_may_have[active] if  suits_mapping[c] != starting_suit}                
            players_may_have[active] = temp
    
    return players_may_have



#def how_many(state, p_id):
#    """ Determines how many cards each player should have in their hand.
#    Returns
#    -------
#    dict
#        A dict mapping player number to number of required cards. 
#    """
#    other_players = [(i + p_id) % 4 for i in range(1, 4)]
#    counts = {p:8 for p in other_players}
#    for p, card in state.player_card_tuples(state.history):
#        if p != p_id:
#            counts[p] -= 1
#        
#    return counts
    
def assign_hands(state, p_hand, p_id):
    """ Returns a dict of possible hands for a player given that we know
    the hand of player p_id. Returns only A plausible solution. """
    card_constraints, number_constraints = inverse_legal_moves(state, p_hand, p_id)
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
        self.card_constraints, self.number_constraints = inverse_legal_moves(state, p_hand, p_id)
        self.card_constraints = propagate_constraints(self.card_constraints, self.number_constraints)
        if not check_solveable(self.card_constraints, self.number_constraints):
            assert(True == False)
        
        if p_id == state.active:
            self.untried_actions = set(iter(state.actions(p_hand)))
        else:
            self.untried_actions = set(self.card_constraints[state.active])
            
    def add_child(self, action):
        new_hand = set(self.p_hand)
        new_state = self.state.result(action)
        if self.state.active == self.p_id:
            new_hand.remove(action)
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
        result = distribute_cards(self.card_constraints, self.number_constraints, check = False)
        result[self.p_id] = set(self.p_hand)
        return result
    
    
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





    