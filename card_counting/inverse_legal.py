# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 13:40:32 2018

@author: martin
"""
from constants import constants as con
import copy
from .distribute_cards import distribute_cards

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
    number_constraints = {p: 8 for p in other_players}
    suits_mapping = con.SUITS_MAPPING[state.game_mode]
    # All other players start with all possible cards that are not in our hand.
    count = 0
    
    # ---------------- stuff to deal with running away ---------------------- #
    if state.game_mode in con.PARTNER_GAMES:
        check_for_running_away = True  # davonlaufen
        called_ace = con.GAME_MODE_TO_ACES[state.game_mode]
        called_suit = suits_mapping[called_ace]
        remaining_cards_of_called_suit = 6
        ace_was_played = False
    else:
        check_for_running_away = False
    # ----------------------------------------------------------------------- #
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
    
        if check_for_running_away:
            if suits_mapping[card] == called_suit:
                remaining_cards_of_called_suit -= 1                
            if starting_suit == called_suit:
                if card == called_ace:
                    ace_was_played = True
                if count == 3 and not ace_was_played:
                    # ran away. 
                    player_who_ran = (p - 3) % 4
                    check_for_running_away = False
                    for p_2 in other_players:
                        if p_2 != player_who_ran:
                            card_constraints[p_2].discard(called_ace)
                            if remaining_cards_of_called_suit == 3:
                                temp = {c for c in card_constraints[p_2] if  suits_mapping[c] != called_suit} 
                                card_constraints[p_2] = temp
        count = (count + 1) % 4     
    return card_constraints, number_constraints


def increment_legal_moves(state, card, players_may_have):
    active = state.active
    players_may_have = copy.deepcopy(players_may_have)
    suits_mapping = con.SUITS_MAPPING[state.game_mode]
    n_played = len(state.history)
    
    for value in players_may_have.values():
        value.discard(card)
    if n_played % 16 != 0:
        round_str = state.history[-n_played:]
        starting_suit = suits_mapping[round_str[1:4]]
        played_suit = suits_mapping[card]
        if played_suit != starting_suit:
            temp = {c for c in players_may_have[active] if  suits_mapping[c] != starting_suit}                
            players_may_have[active] = temp
    
    return players_may_have
    

def assign_hands(state, p_hand, p_id):
    """ Returns a dict of possible hands for a player given that we know
    the hand of player p_id. Returns only A plausible solution. """
    card_constraints, number_constraints = inverse_legal_moves(state, p_hand, p_id)
    result = distribute_cards(card_constraints, number_constraints)
    return result

def filter_equivalent_cards(state, hand):    
    all_categories = con.get_categories(state.game_mode)
    filtered_cards = [card for card in hand if not any(card in cat for cat in all_categories)]
    if len(filtered_cards) == len(hand):
        return filtered_cards
        # No cards in any special category. Bail out early and save computation time. 
    
    temp = [x[1] for x in state.player_card_tuples(state.history)]
    round_start, junk = divmod(len(state.history), 16) # is 4*4
    cards_played_last_rounds = temp[0:round_start * 4]
    
    for cat in all_categories:
        cat_in_hand = sorted([card for card in hand if card in cat], key=lambda x: cat.index(x))
        cat_remaining = [card for card in cat if not card in cards_played_last_rounds]
    
        previous = -2
        # if there are no unplayed cards whose rank is between the two cards in
        # the players hand, then it doesn't matter which card is played. 
        for c in cat_in_hand:
            rank = cat_remaining.index(c)
            if rank != previous + 1:
                filtered_cards += [c]
            previous = rank
        
    return filtered_cards
    
    
    
