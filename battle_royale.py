# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 11:02:00 2018

@author: martin
"""

import math
from itertools import combinations
from multirounds import run_matches

def print_scores(results):
    temp = [(id_dict[i], score) for i, score in results.items()]
    leaderboard = sorted(temp, key = lambda x: -x[1])
    max_len = max([len(str(x[0])) for x in leaderboard])
    print(max_len)
    print("=============== Leaderboard ==================")
    for p, score in leaderboard:
        p_formatted = str(p).ljust(max_len)
        print("{}: {}".format(p_formatted, score))

player_pool = []
n_worlds_list = [4, 8, 10, 15, 20, 50]

for c in [0.5, math.sqrt(2), 2]:
    player_pool += [["MCTSPLUS", {"c": c}]]
    for n in n_worlds_list:
        player_pool += [["PIMC", {"c": c, "n_worlds": n}]]
        
n_players = len(player_pool)

id_dict = {i: player for i, player in enumerate(player_pool)}
n_matches = 4
results = {i: 0 for i in range(n_players)}

count = 0
for perm in combinations(range(n_players), 4):
    tup = ([id_dict[i] for i in perm], n_matches)
    points_totals = run_matches(tup, verbose=True)
    for i, score in points_totals.items():
        results[perm[i]] += score
        
    count += 1
    if count % 100 == 0:
        print_scores(results)
        
print_scores(results)
    

