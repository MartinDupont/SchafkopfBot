# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 11:17:21 2018

@author: martin
"""

from gamestate import GameState
import constants as con
import copy
import random
from bots import DumbBot
from MCTSPlus import MonteCarloPlus, Node, assign_hands, how_many, inverse_legal_moves
from distribute_cards import distribute_cards

#game_mode = "Schellen Solo"
#
#deck = copy.deepcopy(con.ALL_CARDS)
#
#random.shuffle(deck)
#
#hands = {}
#for i in range(4):
#    hands[i] = set(deck[i*8:(i+1)*8])
#    
#state = GameState(game_mode = game_mode, offensive_player = 2, active=0)
#
#bot_list = [DumbBot(), MonteCarloPlus(), DumbBot(), DumbBot()]
#
#agents = {i: bot for i, bot in enumerate(bot_list)}
#
#for i in range(4):
#    agents[i].hand = hands[i]
#
#for i in range(32):
#    active = state.active
#    card = agents[active].play_card(state)
#    state = state.result(card)
    
   # ==========================================================================#
bot = MonteCarloPlus()
    
test_state = GameState(game_mode='Schellen Solo', offensive_player=2, active=1, history='0G101G8_2G7_3GA_3E9_0E101E8_2HA_0SO_1SK_2EO_3HO_2S7_3HU_0S8_1S9_3H8_0H101H7_2H9_0SA_1GU_2EU_3E7_2G9_3EK_0S10', player_points=(31, 0, 28, 23))  
    
test_hand = {'GO_', 'HK_'}
    
test_id = 1

test_node = Node(test_state, test_hand, test_id)

#for i in range(10):
#    try_again = Node(test_state, test_hand, test_id)
#    try_child, _ = bot.expand_node(try_again)
#    print(i)
#    print(try_child)
#    print("++++++++++++++++++++++++++")


new_state = GameState(game_mode='Schellen Solo', offensive_player=2, active=1, history='0G101G8_2G7_3GA_3E9_0E101E8_2HA_0SO_1SK_2EO_3HO_2S7_3HU_0S8_1S9_3H8_0H101H7_2H9_0SA_1GU_2EU_3E7_2G9_3EK_0S101GO_', player_points=(31, 17, 28, 23))
new_hand = {"HK_"}
p_id = 1
for i in range(10):
    print("++++++++++++++++++++++++++++")
    new_hand = {"HK_"}
    card_constraints = inverse_legal_moves(new_state, new_hand, p_id)
    number_constraints = how_many(new_state, p_id)
    print(card_constraints)
    print(number_constraints)
    possible_hands = distribute_cards(copy.deepcopy(card_constraints), copy.deepcopy(number_constraints))
    print(possible_hands)        



