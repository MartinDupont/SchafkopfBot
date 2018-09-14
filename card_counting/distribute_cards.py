"""

"""
from constants import constants as con
import random
from collections import defaultdict

def reorder_constraints(card_constraints):
    """ 
    Parameters
    ----------
    card_constraints: dict of sets
        A dictionary of player_number: possible cards
        
    Returns
    -------
    dict
        A dictionary of card: possible player_numbers
    """
    out = defaultdict(set)
    for p_id, constraints in card_constraints.items():
        for card in constraints:
            out[card].add(p_id)
            
    return out

def unplayed_cards(state, hand):
    unplayed = set(con.ALL_CARDS)
    for p, card in state.player_card_tuples(state.history):
        unplayed.remove(card)
        
    for card in hand:
        unplayed.remove(card)
    return unplayed
        

def check_solveable(card_cons, number_cons):
    """ Check that the supplied problem is solveable.
        This means:
            - There is enough cards to go around.
            - For each player, his number of allowed cards must be greater
              than or equal to the number of cards he needs to be given.
            - Between any pair of players, the size of the union of their
              allowed cards must be greater than or equal to the sum of the
              number of cards they need to be given. """
              
    all_cards = set()
    for key, constraint in card_cons.items():
        if len(constraint) < number_cons[key]:
            return False
        
        other_keys = [k for k in card_cons.keys() if k !=  key]
        double_set = set()
        n = 0
        for k_2 in other_keys:
            double_set.update(card_cons[k_2])
            n += number_cons[k_2]
        if len(double_set) < n:
            return False
        # make this look nice by doing set comprehension on chained sets!!!
        all_cards.update(set(constraint))
    n_possible_cards = len(all_cards)
    n_needed_cards = sum(number_cons.values())
    if not (n_needed_cards == n_possible_cards):
        return False
    return True



## =============================================================================

def only_choice(card_cons, number_cons, inplace = False):
    """ If the size of one players allowed cards is equal to the number of
    cards the player is to be given, then he must be given those cards, and
    they can be removed from the hands of the other players. 
    """
    if inplace:
        #card_cons = copy.deepcopy(card_cons)
        card_cons = {k: set(v) for k, v in card_cons.items()}
    #new_numbers = copy.deepcopy(number_cons)
    keys = list(number_cons.keys())
    # This should be replaced with something that skips empty sets. 
    #keys = keys+keys # this is hacky. 
    for key in keys:
        constraint = card_cons[key]
        if len(constraint) == number_cons[key]:
            # if the only options for this guy are of equal length to the number he needs,
            # then those values cannot be in the other guys hands
            for key_2 in keys:
                if key_2 != key:
                    card_cons[key_2] -= constraint
                    
    return card_cons


def only_choice_pairs(card_cons, number_cons, inplace = False):
    """ If between a pair of players, the size of the union of their possible cards is
    exacly equal to the sum of the number of cards they are to be given, then
    those cards must be shared between the two players, and they can be
    eliminated from the possibilities of the other player."""
    
    if inplace:
        #card_cons = copy.deepcopy(card_cons)
        card_cons = {k: set(v) for k, v in card_cons.items()}

    keys = list(card_cons.keys())
    for key in keys:
        not_keys = [k for k in keys if k != key]
        sum_n = 0
        union_cons = set()
        for k_2 in not_keys:
            sum_n += number_cons[k_2]
            union_cons.update(card_cons[k_2])
            
        if len(union_cons) == sum_n:
            card_cons[key] -= union_cons
    
    return card_cons
            
            
def propagate_constraints(card_cons, number_cons, inplace=False):
    new_cons = only_choice(card_cons, number_cons, inplace)
    new_cons = only_choice_pairs(new_cons, number_cons, inplace)
    return new_cons
          

# ============================================================================



def check_done(solution, number_cons):
    if all(len(v) == number_cons[k] for k, v in solution.items()):
        return True
    return False

def distribute_cards(card_constraints, number_constraints, check=True):
    """ Given a set of possible cards for each player, and a number of cards
    they must be given, find a plausible set of hands for each player.
    The set logic used here is somewhat complicated, I will provide a link
    to a mathematical proof that this algorithm works in the project documents.
    
    Returns
    -------
    dict of int : set()
        A dict of player_number: hand
    """
    
    # -------------------------------------------------------------------------
    # Check if the task is possible, i.e. possible number of cards == cards needed.
    if check:
        if not check_solveable(card_constraints, number_constraints):
            raise ValueError("Unsolveable Conditions")
    # -------------------------------------------------------------------------

    keys = list(number_constraints.keys())
    solution = propagate_constraints(card_constraints, number_constraints)
    
    # only need to look at double sets.
    # double_sets is a list of all cards which are in two or more sets. 
    card_players = reorder_constraints(solution)
    double_sets = {key: value for key, value in card_players.items() if len(value) > 1}
    while not check_done(solution, number_constraints):
        card = random.choice(list(double_sets.keys()))
        players = double_sets.pop(card)
        p = players.pop() 
        # pick any player, it is guaranteed not to matter as long as we propagate constraints correctly.
        for k in keys:
            if k != p:
                solution[k].discard(card)
           
        solution = propagate_constraints(solution, number_constraints, inplace = True)

        card_players = reorder_constraints(solution)
        double_sets = {key: value for key, value in card_players.items() if len(value) > 1}
    return solution
        
        


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
        
    print(result)
        
    pcp = {0: {'GK_', 'G8_', 'H9_', 'H10'},
           2: {'GK_', 'G8_', 'EA_', 'EK_'},
           3: {'EA_', 'EK_'}}
    
    ncp = {0: 2, 2: 2, 3: 2} 
    
    for _ in range(10):    
        result = distribute_cards(pcp, ncp) 
     
    import time
    start = time.time()
        
    pcp = {1: {'E8_', 'E9_', 'G10', 'G8_', 'G9_', 'GA_', 'GK_', 'H10',
                        'H7_', 'H8_', 'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
           2: {'E8_', 'E9_', 'G10', 'G8_', 'G9_', 'GA_', 'GK_', 'H10',
                        'H7_', 'H8_', 'H9_', 'HA_', 'HK_', 'S8_', 'S9_'},
           3: {'G10', 'G8_', 'G9_', 'GA_', 'GK_'}}        
        
    ncp = {1: 5, 2: 5, 3: 5} 
    
    for _ in range(10000):    
        result = distribute_cards(pcp, ncp) 
        
    end= time.time()
    print("Time for trial: "+str(end-start))
    # Previous benchmark is 0.33 seconds for 10000 trials.
        
    print(result)


