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



#def propagate_constraints(card_cons, number_cons):
#    """ 
#    """
#    new_cards = copy.deepcopy(card_cons)
#    new_numbers = copy.deepcopy(number_cons)
#    keys = list(new_numbers.keys())
#    # This should be replaced with something that skips empty sets. 
#    keys = keys+keys # this is hacky. 
#    for key in keys:
#        constraint = new_cards[key]
#        if len(constraint) == new_numbers[key]:
#            # if the only options for this guy are of equal length to the number he needs,
#            # then those values cannot be in the other guys hands
#            for key_2 in keys:
#                if key_2 != key:
#                    new_cards[key_2] -= constraint
#                    
#    # for all the cards in the reduced problem which only have 1 possibility,
#    # add them to the solution directly.
#    temp = reorder_constraints(new_cards)
#    pre_solution = {key: set() for key in new_numbers.keys()}
#    for card, p_ids in temp.items():
#        if len(p_ids) == 1:
#            p = p_ids.pop()
#            pre_solution[p].add(card)
#            new_numbers[p] -= 1 
#            for key in new_numbers.keys():
#                new_cards[key].discard(card)
#    return new_cards, new_numbers, pre_solution


def check_consistent(solution, card_constraints, number_constraints): 
    """ Checks if the solution could satisfy the original problem.
    return false if inconsistent!"""
    for key, value in solution.items():    
        a = set(value).issubset(card_constraints[key])
        b = len(value) == number_constraints[key]
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
        for key, num in number_cons.items():
            solution[key] = set(thing[prev : prev + num])
            prev += num
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
   
def local_solved(card_cons, number_cons):
    keys = number_cons.keys()
    a = all(val <= 0 for val in number_cons.values()) #<= for safety's sake, don't want to iterate past 0. 
    b = all((not card_cons[k]) for k in keys)
    if a and b:
        return True
    return False



def search(card_cons, number_cons):

    """ Assumes solution is in player-first ordering."""
    
    card_cons, number_cons, pre_solution = propagate_constraints(card_cons, number_cons) 
    # This cuts down the problem based on constraint propagation.  
#    print("_____________________________")
#    print(card_cons)
#    print(number_cons)
    # recursive base cases.
    if local_solved(card_cons, number_cons): # if it's solved, return SOMETHINg
        return pre_solution
    if not check_solveable(card_cons, number_cons): # if it's not solveable, return False
        return False
    
    t = trivial_solution(card_cons, number_cons)
    if t:
        return t
    

    temp = reorder_constraints(card_cons)
    chosen_card, players = min( temp.items() , key = lambda x: len(x[1])) # will be either 3 or 2. 
    # choose the next card to assign based on the Variable that is most constrained. 
#        ordered = sorted(players, key= lambda x: -(number_cons[x] - len(solution[x])))
#        # then investigate the assignments starting with the LEAST constraining.
    
    for p_num in players: 
        new_card_cons = copy.deepcopy(card_cons)
        new_num_cons = copy.deepcopy(number_cons)
        
        new_num_cons[p_num] -= 1
        for p_2 in players:
            new_card_cons[p_2].remove(chosen_card)
        solution = search(new_card_cons, new_num_cons)
        if solution:
            for key, value in pre_solution.items():
                solution[key].update(value)
            solution[p_num].add(chosen_card)
            return solution
        # if we find a solution at the bottom, we propagate back up the tree,
        # adding the assignments in as we go. At the top, we yield the full solution

#def distribute_cards(card_cons, number_cons):
#    solution = search(card_cons, number_cons)
#    if solution:
#        return solution
#    else:
#        assert (True == False)


# =============================================================================
def conflicts(solution, cpc):
    """ Takes reordered card conditions """
    conflicted = []
    for card, player in solution.items():
        if not player.issubset(cpc[card]):
            conflicted += [card]
    return conflicted

def try_swap(solution, c_1, c_2):
    sol = copy.deepcopy(solution)
    p_1, p_2 = sol[c_1], sol[c_2]
    sol[c_1] = p_2
    sol[c_2] = p_1
    return sol

def all_combinations(solution, conflicted_cards, all_cards, cpc):
    for c_1 in conflicted_cards:
        for c_2 in all_cards:
            if c_1 != c_2:
                new = try_swap(solution, c_1, c_2)
                new_conflicts = conflicts(new, cpc)
                if len(new_conflicts) < len(conflicted_cards):
                    solution = new
                    conflicted_cards = new_conflicts
                    return solution, conflicted_cards
                    
    return None, None


def distribute_cards(card_constraints, number_constraints):
    # -------------------------------------------------------------------------
    # Check if the task is possible, i.e. possible number of cards == cards needed.
    all_cards = set()
    for key, constraint in card_constraints.items():
        assert( len(constraint) >= number_constraints[key]), "Unsolveable conditions."
        other_keys = [k for k in card_constraints.keys() if k !=  key]
        double_set = set()
        n = 0
        for k_2 in other_keys:
            double_set.update(card_constraints[k_2])
            n += number_constraints[k_2]
        assert (len(double_set) >= n), "Unsolveable conditions 2nd order."
        # make this look nice by doing set comprehension on chained sets!!!
        all_cards.update(set(constraint))
    n_possible_cards = len(all_cards)
    n_needed_cards = sum(number_constraints.values())
    assert (n_needed_cards == n_possible_cards), "Unsolveable conditions."
    # -------------------------------------------------------------------------

    # Copy passed variables so that they are not changed
    card_cons = propagate_constraints(card_constraints, number_constraints)
    number_cons = copy.deepcopy(number_constraints)
    cpc = reorder_constraints(card_cons)

    #print(cpc)
    # Generate initial state in a dumb way
    solution = {}
    all_cards = list(all_cards)
    prev = 0
    for key, num in number_cons.items():
        for c in all_cards[prev : prev + num]:
            solution[c] = {key}
        prev += num
 
    #solution = reorder_constraints(temp_solution)
    conflicted_cards = conflicts(solution, cpc)
    while conflicted_cards:
        new_sol, new_conflicts = all_combinations(solution, conflicted_cards, all_cards, cpc)
        if new_sol:
            solution = new_sol
            conflicted_cards = new_conflicts
        
        else:
                        
            print("==== no local improvement ======" )
            print(conflicted_cards)
            print(reorder_constraints(solution))
            print(number_cons)
            print(card_cons)
            c_1 = random.choice(conflicted_cards)
            c_2 = random.choice([card for card in all_cards if card != c_1])
            solution = try_swap(solution, c_1, c_2)
            conflicted_cards = conflicts(solution, cpc)

#    print(solution) 
    return reorder_constraints(solution)
    

            


## =============================================================================

def only_choice(card_cons, number_cons):
    """ If the size of one players allowed cards is equal to the number of
    cards the player is to be given, then he must be given those cards, and
    they can be removed from the hands of the other players. 
    """
    new_cards = copy.deepcopy(card_cons)
    #new_numbers = copy.deepcopy(number_cons)
    keys = list(number_cons.keys())
    # This should be replaced with something that skips empty sets. 
    #keys = keys+keys # this is hacky. 
    for key in keys:
        constraint = new_cards[key]
        if len(constraint) == number_cons[key]:
            # if the only options for this guy are of equal length to the number he needs,
            # then those values cannot be in the other guys hands
            for key_2 in keys:
                if key_2 != key:
                    new_cards[key_2] -= constraint
                    
    return new_cards


def only_choice_pairs(card_cons, number_cons):
    """ If between a pair of players, the size of the union of their possible cards is
    exacly equal to the sum of the number of cards they are to be given, then
    those cards must be shared between the two players, and they can be
    eliminated from the possibilities of the other player"""
    
    new_cards = copy.deepcopy(card_cons)

    keys = list(card_cons.keys())
    for key in keys:
        not_keys = [k for k in keys if k != key]
        sum_n = 0
        union_cons = set()
        for k_2 in not_keys:
            sum_n += number_cons[k_2]
            union_cons.update(new_cards[k_2])
            
        if len(union_cons) == sum_n:
            new_cards[key] -= union_cons
    
    return new_cards
            
            
def propagate_constraints(card_cons, number_cons):
    
    stalled = False
    old_cons = card_cons
    while not stalled:
        new_cons = only_choice(card_cons, number_cons)
        new_cons = only_choice_pairs(new_cons, number_cons)
        if new_cons == old_cons:
            stalled = True
        old_cons = new_cons
    return new_cons
          

# ============================================================================


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
#    card_constraints = propagate_constraints(card_constraints, number_constraints)
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
#    for _ in range(sum(list(ncp.values())) - len(p123)):
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
#    print(distributedCards)
#    for key, value in distributedCards.items():    
#        assert(set(value).issubset(card_constraints[key])), "Someone was given inconsistent cards."
#        assert(len(value) == number_constraints[key]), "Someone was given the wrong number of cards."
#    
#    distributedCards = {key:set(value) for key, value in distributedCards.items()}
#    return distributedCards

if __name__ == "__main__":
#        pcp = {1: [1,3,4,6,7,8,9], 2: [1,2,4,5,7,8,9], 3: [2,3,5]}
#        ncp = {1: 3, 2: 3, 3: 3}
#    pcp = {0: {'EA_', 'SU_'}, 2: {'GK_', 'SU_'}, 3: {'EA_'}}
#    ncp = {0: 1, 2: 1, 3: 1}
#    for _ in range(10):
#        result = distribute_cards(pcp, ncp)
#        print(result)
#        
    pcp = {2: {'GK_', 'SU_'}, 3: {'EA_'}, 0: {'EA_', 'SU_'}}
    ncp = {2: 1, 3: 1, 0: 1}
    for _ in range(10):    
        result = distribute_cards(pcp, ncp)
        
    pcp = {0: {'GK_', 'G8_', 'H9_', 'H10'},
           2: {'GK_', 'G8_', 'EA_', 'EK_'},
           3: {'EA_', 'EK_'}}
    
    ncp = {0: 2, 2: 2, 3: 2} 
    import time
    start = time.time()
    for _ in range(1000):    
        result = distribute_cards(pcp, ncp) 
        
    end= time.time()
    print("Time for trial: "+str(end-start))
        
        
    print(result)


