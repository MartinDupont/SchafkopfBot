# -*- coding: utf-8 -*-
"""
Runs Multiple matches in parallel.


@author: martin
"""
from multiprocessing import Pool
from environments import Arena
from os import cpu_count


def parallel_matches(bots_list, n_matches):
    n_cores = cpu_count()
    temp_list = [int(n_matches/n_cores) for i in range(n_cores)]
    temp_list[0] += n_matches % n_cores 
    match_list = [(bots_list, t) for t in temp_list]

    pool = Pool()
    results = pool.map(run_matches, match_list) 
    final_scores = {i:0 for i in range(4)}
    for r in results:
        for p, score in r.items():
            final_scores[p] += score
    return final_scores

def run_matches(tup, verbose=False):
    bots_list = tup[0]
    n_matches = tup[1]
    arena = Arena(bots_list)
    
    for i in range(n_matches):
        arena.new_game(verbose = verbose)
        
    return arena.points_totals



if __name__ == "__main__":        
 
    n_matches = 40
        
    #botstring = ["MCTSPLUS", "PIMC", "MCTSPLUS", "PIMC" ]
    bots_list = ["MCTSPLUS", "PIMC", "DUMB", "DUMB"]
    #bots_list = ["MCTSPLUS", "PIMC", "MCTSPLUS", "PIMC"]
    #bots_list = ["MCTSPLUS", "MCTSPLUS", "PIMC", "PIMC" ]
    result = parallel_matches(bots_list, n_matches)
    print("=== Final Scores ===")
    print("n_matches: {}".format(n_matches))
    print("--------------------")
    for i in range(4):
        print(str(i)+": "+bots_list[i]+": {}".format(result[i]))
    


