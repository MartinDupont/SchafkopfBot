# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:02:00 2018

@author: martin
"""

import math
from itertools import permutations
from multirounds import run_matches

player_pool = [["DUMB", {}]]
n_worlds_list = [1, 4, 8, 10, 15, 20, 50, 100]

for c in [0.25, 0.5, math.sqrt(2), 1.0]:
    player_pool += [["MCTSPLUS", {"c": c}]]
    for n in n_worlds_list:
        player_pool += [["PIMC", {"c":c, "n_worlds": n}]]
        
n_players = len(player_pool)

id_dict = {i: player for i, player in enumerate(player_pool)}
n_matches = 1
results = {i: 0 for i in range(n_players)}

for perm in permutations(range(n_players), 4):
    # We choose permutations because player order matters.
    tup = ([id_dict[i] for i in perm], n_matches)
    print("========== new pairs ========")
    print(perm)
    print(tup)
    points_totals = run_matches(tup, verbose=True)
    for i, score in points_totals.items():
        results[perm[i]] += score
    print(results)
        
print("========== Final scores ===========")
for i, score in results.items():
    print("{} : {}".format(id_dict[i], score))
    

