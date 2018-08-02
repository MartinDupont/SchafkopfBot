# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 12:42:28 2018

@author: martin
"""

import random
import copy
import numpy as np
import constants as con
import math
import time

class BaseBot():
    def __init__(self):
        self._hand = None
    
    def reset(self):
        self.hand = None
    # ------------------------------------------------
    def get_hand(self):
        return self._hand
    
    def set_hand(self, hand): 
        if not (hand is None):
            if not all([a in con.ALL_CARDS for a in hand]):
                raise ValueError("These aren't valid cards")
        self._hand = hand
    hand = property(get_hand, set_hand)
    # -------------------------------------------       
            
    def aces_in_hand(self):
        return [a for a in self.hand if a[1] == 'A']

    def play_card(self, state):
        raise NotImplementedError
    
    def play_or_not(self):
        raise NotImplementedError
    
    def play_with(self):
        raise NotImplementedError
# =========================================================================== # 
class DumbBot(BaseBot):
    """ Just plays randomly."""
            
    def play_or_not(self):
        options = [True, False]
        return random.choice(options)
    
    def play_with(self, i): 
        my_aces = self.aces_in_hand()
        temp_dict = {"Partner Schellen": "SA_", "Partner Eichel": "EA_",
                     "Partner Gras": "GA_"}
        allowable_partner_games = [key for key, value in temp_dict.items() 
                                    if not value in my_aces]

        
        return random.choice(['Wenz', 'Herz Solo', 'Gras Solo', 'Eichel Solo',
                              'Schellen Solo'] + allowable_partner_games 
                                + allowable_partner_games 
                                + allowable_partner_games
                                + allowable_partner_games
                                + allowable_partner_games
                                + allowable_partner_games
                                + allowable_partner_games) 
                                # cheap way of making sure they don't just play
                                # solos all the time. 
    
        
    #---------------------------------------------------------------------
    def play_card(self, state):
        card = random.choice(state.actions(self.hand))
        self.hand.remove(card)
        return card
       
# =========================================================================== #        

class ProxyBot(BaseBot):
    """ Plays with human input. For debugging purposes, and for playing 
    against real opponents at card tables"""
    
    def play_card(self, state):
        # Note that this function doesn't need to know the proxybot's hand. 
        # This is so that we can play against opponents whose hands we dont know.
        while True:
            play = input("Which card would player {} like to play? \n".format(state.active))
            if len(play) == 2:
                play = play + "_"
            if play in con.ALL_CARDS:
                return play
            else:
                print("{} is not a valid card".format(play))
                
        return play

    def play_or_not(self):
        play = input("""Would like to play?: \n1: Play \n2: Don't play \n""")
        if play == "1":
            return True
        return False
    
    def play_with(self, i):
        while True:
            input_string = "Player {} would like to play a: \n".format(i)
            option_dict = {}
            j = 0
            for  g in con.GAME_MODES:
                if g != "Ramsch":
                    input_string += str(j)+": "+g+"\n"
                    option_dict[j] = g
                j += 1
                
            option_dict[str(i)] = "Ramsch" 
            # Ramsch will be an option for if players misspeak (as often happens over beers),
            # such that they can elect not to play after just having played. 
            input_string += str(j)+": Cancel \n" # may or may not be necessary
            play = input(input_string)
            try:
                return option_dict[play]
            except KeyError:
                print("That is not a valid choice")
                continue
        
# =============================================================================
 
def unplayed_cards(state, hand):
    unplayed = set(copy.deepcopy(con.ALL_CARDS))
    for p, card in state.player_card_tuples(state.history):
        unplayed.remove(card)
        
    for card in hand:
        unplayed.remove(card)
    return unplayed
        


               
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
            self.untried_actions = unplayed_cards(state, p_hand)
            
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
        thing += ("State: "+str(self.state)+"\n")
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


class MonteCarlo(DumbBot):
    """ Follows a very straightfoward implementation of a Monte Carlo Tree Search:
    https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    
    The algorithm had to be modified slightly, because schafkopf is an incomplete
    information game. Opponents can play any of the cards that have not been 
    played so far, and that are not known to be in this players hand. 
    As it stands, this is inefficient, as we can rule out that other players
    have certain hands. 
    """
    def __init__(self):
        super().__init__()
        self.root_node = None
        self.player_id = None
        
    def play_or_not(self):
        return False
    
    # -------------------------  
    def tree_policy(self, node):
        while not node.state.terminal_test():
            if not node.is_fully_expanded():
                return self.expand_node(node)
            else:
                node, _ = self.best_child(node)
        return node   
    
    def default_policy(self, state, hand, p_id):
        # I think, assigning people random consistent hands would be better 
        # than this. These predictions are way off. 
        hand = set(hand)
        while not state.terminal_test():
            active = state.active
            if p_id == active:
                action = random.choice(state.actions(hand))
                hand.remove(action)
            else:
                action = random.choice(list(unplayed_cards(state, hand)))
            state = state.result(action)
        return state.utilities()
    
    def back_up(self, node, utils):
        while not(node.parent is None):
            p_num = node.parent.state.active
            node.N += 1
            node.Q += utils[p_num]
            node = node.parent  
        node.N += 1
            
    def expand_node(self, input_node):
        a = input_node.untried_actions.pop()
        new_node = input_node.add_child(a)
        return new_node
            
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
        i=0
        start = time.time()
        t = time.time() - start
        while t < 2:
            #print(i)
            v = self.tree_policy(self.root_node)
            utils = self.default_policy(v.state, v.p_hand, v.p_id)
            self.back_up(v, utils)
            node, action = self.best_child(self.root_node, 0)
            choice = action
            t = time.time() - start
            i+=1
        #self.root_node.print_tree()
        #print("Number of nodes expanded: {}".format(i))
        self.hand.remove(choice)
        return choice


class MonteCarloPlus(MonteCarlo):
    def default_policy(self, state, hand, p_id):
        # I think, assigning people random consistent hands would be better 
        # than this. These predictions are way off. 
        hand = set(hand)
        while not state.terminal_test():
            active = state.active
            if p_id == active:
                action = random.choice(state.actions(hand))
                hand.remove(action)
            else:
                action = random.choice(list(unplayed_cards(state, hand)))
            state = state.result(action)
        return state.utilities_test()      
