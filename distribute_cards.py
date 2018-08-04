"""

"""
import random
from collections import defaultdict
import copy
from itertools import cycle

def reorder_constraints(card_constraints):
    out = defaultdict(set)
    for p_id, constraints in card_constraints.items():
        for card in constraints:
            out[card].add(p_id)
            
    return out


def propagate_constraints(card_cons, number_cons):
    """ Assuming solution is in the card-first representation.
    """
    new_cons = copy.deepcopy(card_cons)
    for key, constraint in new_cons.items():
        if len(constraint) == number_cons[key]:
            # if the only options for this guy are of equal length to the number he needs,
            # then those values cannot be in the other guys hands
            not_key = [k for k in new_cons.keys() if key != k]
            for k in not_key:
                new_cons[k] -= constraint
    
    return new_cons


def check_consistent(solution, card_constraints, number_constraints): 
    """ Checks if the solution could satisfy the original problem.
    return false if inconsistent!"""
    for key, value in solution.items():    
        a = set(value).issubset(card_constraints[key])
        b = len(value) <= number_constraints[key]
    if not (a and b):
        return False
    return True
 
def check_solveable(card_cons, number_cons):
    """ Check that the supplied PARTIAL problem is solveable.
    I have an inkling that between check_consistent, and check_solveable, 
    one may be redundant. """
    superset = set()
    for key, constraint in card_cons.items():
        if len(constraint) < number_cons[key]:
            return False
        superset.update(set(constraint))
        
    n_possible_cards = len(superset)
    n_needed_cards = sum(number_cons.values())
    if not(n_needed_cards == n_possible_cards):
        return False
    
    return True 

def trivial_solution(card_cons, number_cons):
    """ Check if the supplied PARTIAL problem may be solved trivially."""
    superset = set()
    for key, constraint in card_cons.items():
        superset.update(constraint)
    if all(constraint == superset for constraint in card_cons.values()):
        thing = list(superset)
        solution = {}
        prev = 0
        for key, num in number_cons:
            solution[key] = thing[prev : prev + num]
            num = prev
        return solution
    else:
        return False

def solved(solution, number_constraints, card_constraints):
    """ Check that the provided solution satisfies the ORIGINAl constraints. """
    a = all(number_constraints[key] == len(value) for key, value in solution.items())
    b = all(value.issubset(card_constraints[key]) for key, value in solution.items())
    
    if a and b :
        return True
    return False
   


def distribute_cards(card_constraints, number_constraints):

    # ------------------------------------------------------------------------
    def search(solution, card_cons, number_cons):
        """ Assumes solution is in player-first ordering."""
        solution = copy.deepcopy(solution)
        card_cons = copy.deepcopy(card_cons)
        number_cons = copy.deepcopy(number_cons) # paranoid.
        # recursive base cases. The order is important.
        if not check_solveable(card_constraints, number_constraints):
            return False
        if solved(solution, number_constraints):
            return solution
#        thing = trivial_solution(card_constraints, number_constraints)
#        if thing:
#            return thing
        
        card_cons = propagate_constraints(card_cons, number_cons)
        temp = reorder_constraints(card_constraints)
        
        # for all the cards in the reduced problem which only have 1 possibility,
        # add them to the solution directly.
        to_delete = []
        for card, p_ids in temp.items():
            if len(p_ids) == 1:
                p = p_ids.pop()
                solution[p].add(card)
                to_delete += [card]
                number_cons[p] -= 1 
        for card in to_delete:
            del temp[card]
         
        if solved(solution, number_constraints):
            return solution. 
        chosen_card, players = min( temp.items() , key = lambda x: len(x[1])) # will be either 3 or 2. 
        # choose the next card to assign based on the Variable that is most constrained. 
#        ordered = sorted(players, key= lambda x: -(number_cons[x] - len(solution[x])))
#        # then investigate the assignments starting with the LEAST constraining.
        
        for p_num in players: 
            new_card_cons = copy.deepcopy(card_constraints)
            new_num_cons = copy.deepcopy(number_constraints)
            new_solution = copy.deepcopy(solution)
            
            new_num_cons[p_num] -= 1
            new_card_cons[p_num].remove(chosen_card)
            
            new_solution[p_num].add(chosen_card)
            thing = search(new_solution, new_card_cons, new_num_cons)
            if thing:
                return thing
    # ------------------------------------------------------------------------  
        

    solution = {}
    for key in card_constraints.keys():
        solution[key] = set()
        
    result = search(solution, card_constraints, number_constraints)
    return result

# =============================================================================
#def distribute_cards(card_constraints, number_constraints):
#    keys = list(number_constraints.keys())
#
#    # Check if the task is possible, i.e. possible number of cards == cards needed.
#    superset = set()
#    for key, constraint in card_constraints.items():
#        assert( len(constraint) >= number_constraints[key]), "Unsolveable conditions."
#        superset.update(set(constraint))
#    n_possible_cards = len(superset)
#    n_needed_cards = sum(number_constraints.values())
#    assert (n_needed_cards == n_possible_cards), "Unsolveable conditions."
#
#    # Copy passed variables so that they are not changed
#    pcp = copy.deepcopy(card_constraints)
#    ncp = copy.deepcopy(number_constraints)
#
#    solution = {}
#    single_sets = {
#    keys[0]: list( pcp[keys[0]] - pcp[keys[1]] - pcp[keys[2]] ),
#    keys[1]: list( pcp[keys[1]] - pcp[keys[0]] - pcp[keys[2]] ),
#    keys[2]: list( pcp[keys[2]] - pcp[keys[0]] - pcp[keys[1]] ) }
#    
#    cpc = reorder_constraints(pcp)
#    
#    for key in keys:
#        for card in single_sets[key]:
#            solution[card] = key
#            
#    for card in superset:
#        if not card in solution:
#            p = max(ncp.keys(), key= lambda x: ncp[x])
#            solution[card] = p
#            ncp[p] -= 1
#            
#    # solution is now a locally assigned solution. 
#    
#    conflicted_cards = {card for card, p in solution.items() if not (p in cpc[key]) }
#
#    while confilcted_cards:
#        c_1, c_2  = 1, 2
#        
#        # do we know that greedy search works???
#
#
## =============================================================================
#
#
#def pick_biggest_double_set(double_sets):
#    keys = list( double_sets.keys() )
#    random.shuffle(keys) # make random initial pick
#    ret = keys[0]
#    for key in keys:
#        if len(double_sets[key]) > len(double_sets[ret]): ret = key
#    return ret
#
#def append_card_decrease_count(card, key, distributedCards, number_of_cards_for_player):
#    distributedCards[key].append(card)
#    number_of_cards_for_player[key] = number_of_cards_for_player[key] - 1
#
#
#def distribute_cards(card_constraints, number_constraints):
#    # card_constraints  - dict, keys: player number, values: list of possible cards for the player
#    # number_constraints - dict, keys: player number, values: integer number of cards needed
#
#    keys = list(number_constraints.keys())
#
#    # Check if the task is possible, i.e. possible number of cards == cards needed.
#    superset = set()
#    for key, constraint in card_constraints.items():
#        assert( len(constraint) >= number_constraints[key]), "Unsolveable conditions."
#        superset.update(set(constraint))
#    n_possible_cards = len(superset)
#    n_needed_cards = sum(number_constraints.values())
#    assert (n_needed_cards == n_possible_cards), "Unsolveable conditions."
#
#    # Copy passed variables so that they are not changed
#    pcp = copy.deepcopy(card_constraints)
#    ncp = copy.deepcopy(number_constraints)
#
#    # turn values of pcp from list to set
#    for key in pcp.keys():
#        pcp[key] = set(pcp[key])
#
#    # Cards every player can have. For now it is a set, later it will become a list.
#    p123 = pcp[keys[0]] & pcp[keys[1]] & pcp[keys[2]]
#    # Cards two out of three players can have; note that values are lists.
#    double_sets = {
#        (keys[0], keys[1]): list( (pcp[keys[0]] & pcp[keys[1]]) - p123 ),
#        (keys[1], keys[2]): list( (pcp[keys[1]] & pcp[keys[2]]) - p123 ),
#        (keys[0], keys[2]): list( (pcp[keys[0]] & pcp[keys[2]]) - p123 ) }
#    # Cards only one player can have; note that values are lists.
#    single_sets = {
#        keys[0]: list( pcp[keys[0]] - pcp[keys[1]] - pcp[keys[2]] ),
#        keys[1]: list( pcp[keys[1]] - pcp[keys[0]] - pcp[keys[2]] ),
#        keys[2]: list( pcp[keys[2]] - pcp[keys[0]] - pcp[keys[1]] ) }
#
#    # Assign the single cards to the players, and adjust ncp (number_of_cards_for_player) accordingly.
#    distributedCards = {key: single_sets[key] for key in keys}
#    for key in ncp.keys():
#        ncp[key] = ncp[key] - len(single_sets[key])
#
#    # Repeat until the cards in double_sets are all distributed.
#    for _ in range(np.sum(list(ncp.values())) - len(p123)):
#        key_pair = pick_biggest_double_set(double_sets)
#        card = random.choice(double_sets[key_pair])
#        double_sets[key_pair].remove(card)
#
#        if ncp[key_pair[0]] > ncp[key_pair[1]]:
#            append_card_decrease_count(card, key_pair[0], distributedCards, ncp)
#        else:
#            append_card_decrease_count(card, key_pair[1], distributedCards, ncp)
#
#    # Change p123 from set to list.
#    p123 = list(p123)
#    while(p123):
#        card = random.choice(p123)
#        p123.remove(card)
#        if ncp[keys[0]]:
#            append_card_decrease_count(card, keys[0], distributedCards, ncp)
#        elif ncp[keys[1]]:
#            append_card_decrease_count(card, keys[1], distributedCards, ncp)
#        elif ncp[keys[2]]:
#            append_card_decrease_count(card, keys[2], distributedCards, ncp)
#
#    for key, value in distributedCards.items():    
#        assert(set(value).issubset(possible_cards_for_player[key])), "Someone was given inconsistent cards."
#        assert(len(value) == number_of_cards_for_player[key]), "Someone was given the wrong number of cards."
#    
#    return distributedCards

if __name__ == "__main__":
#        pcp = {1: [1,3,4,6,7,8,9], 2: [1,2,4,5,7,8,9], 3: [2,3,5]}
#        ncp = {1: 3, 2: 3, 3: 3}
    pcp = {0: {'EA_', 'SU_'}, 2: {'GK_', 'SU_'}, 3: {'EA_'}}
    ncp = {0: 1, 2: 1, 3: 1}
    for _ in range(10):
        result = distribute_cards(pcp, ncp)
        print(result)
        
    pcp = {2: {'GK_', 'SU_'}, 3: {'EA_'}, 0: {'EA_', 'SU_'}}
    ncp = {2: 1, 3: 1, 0: 1}
    for _ in range(10):    
        result = distribute_cards(pcp, ncp)
        print(result)

