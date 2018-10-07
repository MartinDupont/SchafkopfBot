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
    
    # ---------------- stuff to deal with parnter games --------------------- #
    if state.game_mode in con.PARTNER_GAMES:
        check_for_called_ace = True  # davonlaufen
        called_ace = con.GAME_MODE_TO_ACES[state.game_mode]
        called_suit = suits_mapping[called_ace]
        remaining_cards_of_called_suit = 6
        ace_was_played = False
    else:
        check_for_called_ace = False
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
        
        if check_for_called_ace:
            if suits_mapping[card] == called_suit:
                remaining_cards_of_called_suit -= 1                
            if starting_suit == called_suit:
                if card == called_ace:
                    ace_was_played = True
                    check_for_called_ace = False
                elif count != 0 and p != p_id:
                    # If anyone but the first player doesn't play the called
                    # ace, then they cannot have it. 
                    card_constraints[p].discard(called_ace)
                if count == 3 and not ace_was_played:
                    # The guy who opened must have run away. 
                    player_who_ran = (p - 3) % 4
                    check_for_called_ace = False
                    for p_2 in other_players:
                        if p_2 != player_who_ran:
                            if remaining_cards_of_called_suit == 3:
                                # You can only run away if you have 4 or more
                                # of the called colour.
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
    
def filter_playable_cards(card_constraints, number_constraints, player, starting_suit, game_mode):
    """ Given the list of card constraints, i.e. cards a player may have, it
    is quite hard to figure out what cards they may play in a given situation. 
    Despite not knowing exactly what cards they have, we can sometimes narrow
    down our choices for what they can and cannot play. This will handily
    reduce the size of the search tree."""
    
    card_constraints = {p: set(cards) for p, cards in card_constraints.items()}
    suits_mapping = con.SUITS_MAPPING[game_mode]
    other_players = [p for p in card_constraints.keys() if p != player]
    other_players_may_have = (card_constraints[other_players[0]] |
                              card_constraints[other_players[1]])
    only_this_player_can_have = card_constraints[player].difference(other_players_may_have)
    if game_mode in con.PARTNER_GAMES:
        called_ace = con.GAME_MODE_TO_ACES[game_mode]
        called_suit = con.GAME_MODE_TO_SUITS[game_mode]
        
    if starting_suit == None:
        if game_mode in con.PARTNER_GAMES and called_ace in card_constraints[player]:
            n_cards_called_colour = sum(suits_mapping[c] == called_suit
                                         for c in card_constraints[player])
            if called_ace in only_this_player_can_have or (
                    number_constraints[player] == len(card_constraints[player])):
                # combinatoric possibility is covered by this possibility if
                # constraints are propagated. 

                if n_cards_called_colour < 4:
                    return {c for c in card_constraints[player] if 
                            (c == called_ace) or (suits_mapping[c] != called_suit)}
                    # can open with the ace, but not any other card of the called
                    # colour, unless I run away. 
        return card_constraints[player]
    
    possible_cards_of_played_suit = {c for c in card_constraints[player] if
                                      suits_mapping[c] == starting_suit}


    if game_mode in con.PARTNER_GAMES and starting_suit == called_suit:
        if called_ace in only_this_player_can_have:
            # This guy is the only guy who can have the ace. 
            return {called_ace}
        
    # NEED to refactor this. One logic for parnter games, another for the others.
        
    only_this_player_suit = {c for c in only_this_player_can_have if suits_mapping[c] == starting_suit}
    n_cards_possible = len(card_constraints[player])
    n_cards_of_played_suit = len(possible_cards_of_played_suit)
    if (number_constraints[player] > n_cards_possible - n_cards_of_played_suit) or only_this_player_suit:
        # There is no universe in which the player in question is free.
        # Either there is no combinatoric way of dealing him a hand without 
        # a card of the played suit, or there is a card which only he may
        # have which matches the suit. 
        return possible_cards_of_played_suit
    else:
        # There is a possibility that the player is free.
        if game_mode in con.PARTNER_GAMES and starting_suit != called_suit:
            return {c for c in card_constraints[player] if c != called_ace}
        return card_constraints[player]
