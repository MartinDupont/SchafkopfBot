"""
@Author: Juraj Vrabel

All credit to my friend Juraj who helped me with my robot and wrote this function.
It is by far mostly his work, with a couple of minor changes by me. 

"""
import random
import numpy as np
import copy

def pick_biggest_double_set(double_sets):
    keys = list( double_sets.keys() )
    random.shuffle(keys) # make random initial pick
    ret = keys[0]
    for key in keys:
        if len(double_sets[key]) > len(double_sets[ret]): ret = key
    return ret

def append_card_decrease_count(card, key, distributedCards, number_of_cards_for_player):
    distributedCards[key].append(card)
    number_of_cards_for_player[key] = number_of_cards_for_player[key] - 1


def distribute_cards(possible_cards_for_player, number_of_cards_for_player):
    # possible_cards_for_player  - dict, keys: player number, values: list of possible cards for the player
    # number_of_cards_for_player - dict, keys: player number, values: integer number of cards needed

    keys = list(possible_cards_for_player.keys())

    # Check if the task is possible, i.e. possible number of cards == cards needed.
    superset = set()
    for values in possible_cards_for_player.values():
        superset.update(set(values))
        
    n_possible_cards = len(superset)
    n_needed_cards = np.sum(list(number_of_cards_for_player.values()))
    
    assert(n_possible_cards == n_needed_cards), "Unsolvable conditions."

    # Copy passed variables so that they are not changed
    pcp = copy.deepcopy(possible_cards_for_player)
    ncp = copy.deepcopy(number_of_cards_for_player)

    # turn values of pcp from list to set
    for key in pcp.keys():
        pcp[key] = set(pcp[key])

    # Cards every player can have. For now it is a set, later it will become a list.
    p123 = pcp[keys[0]] & pcp[keys[1]] & pcp[keys[2]]
    # Cards two out of three players can have; note that values are lists.
    double_sets = {
        (keys[0], keys[1]): list( (pcp[keys[0]] & pcp[keys[1]]) - p123 ),
        (keys[1], keys[2]): list( (pcp[keys[1]] & pcp[keys[2]]) - p123 ),
        (keys[0], keys[2]): list( (pcp[keys[0]] & pcp[keys[2]]) - p123 ) }
    # Cards only one player can have; note that values are lists.
    single_sets = {
        keys[0]: list( pcp[keys[0]] - pcp[keys[1]] - pcp[keys[2]] ),
        keys[1]: list( pcp[keys[1]] - pcp[keys[0]] - pcp[keys[2]] ),
        keys[2]: list( pcp[keys[2]] - pcp[keys[0]] - pcp[keys[1]] ) }

    # Assign the single cards to the players, and adjust ncp (number_of_cards_for_player) accordingly.
    distributedCards = {key: single_sets[key] for key in keys}
    for key in ncp.keys():
        ncp[key] = ncp[key] - len(single_sets[key])

    # Repeat until the cards in double_sets are all distributed.
    for _ in range(np.sum(list(ncp.values())) - len(p123)):
        key_pair = pick_biggest_double_set(double_sets)
        card = random.choice(double_sets[key_pair])
        double_sets[key_pair].remove(card)

        if ncp[key_pair[0]] > ncp[key_pair[1]]:
            append_card_decrease_count(card, key_pair[0], distributedCards, ncp)
        else:
            append_card_decrease_count(card, key_pair[1], distributedCards, ncp)

    # Change p123 from set to list.
    p123 = list(p123)
    while(p123):
        card = random.choice(p123)
        p123.remove(card)
        if ncp[keys[0]]:
            append_card_decrease_count(card, keys[0], distributedCards, ncp)
        elif ncp[keys[1]]:
            append_card_decrease_count(card, keys[1], distributedCards, ncp)
        elif ncp[keys[2]]:
            append_card_decrease_count(card, keys[2], distributedCards, ncp)

    for key, value in distributedCards.items():    
        assert(set(value).issubset(possible_cards_for_player[key])), "Someone was given inconsistent cards."
        assert(len(value) == number_of_cards_for_player[key]), "Someone was given the wrong number of cards."
    
    return distributedCards

if __name__ == "__main__":
    for _ in range(1000):
#        pcp = {1: [1,3,4,6,7,8,9], 2: [1,2,4,5,7,8,9], 3: [2,3,5]}
#        ncp = {1: 3, 2: 3, 3: 3}
#        print(distributeCards(pcp, ncp))
        remaining_cards = ["H7", "H8", "H9", "H10", "HK", "HA",
                           "E8", "E9", "S8", "S9", 
                           "G8", "G9", "G10", "GA", "GK"]
        pcp = {0: remaining_cards, 1: remaining_cards, 2: ["G8", "G9", "G10", "GA", "GK"]}
        ncp = {0: 5, 1: 5, 2: 5}
        result = distribute_cards(pcp, ncp)
        for key in ncp.keys():
            try:
                assert(len(result[key]) == ncp[key])
            except:    
                print(result)
