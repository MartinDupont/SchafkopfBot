# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:48:20 2018

@author: martin
"""

from environments import Arena

#botstring = ["MCTS", "MCTSPLUS", "DUMB", "DUMB"]
botstring = ["DUMB", "DUMB", "DUMB", "DUMB"]
#botstring = ["MCTSPLUS", "MCTSPLUS", "MCTSPLUS", "MCTSPLUS" ]

arena = Arena(botstring)

for i in range(0):
    arena.new_game(verbose = True)

    print("Round end total points:")  
    print(arena.points_totals)
    
 
dumb_v_smart = arena.points_totals
    
botstring = ["MCTSPLUS", "PIMC", "PRUNING", "PIMC" ]

arena = Arena(botstring)
for i in range(200):
    arena.new_game(verbose = True)

    print("Round end total points:")  
    print(arena.points_totals)
    
smart_v_smarter = arena.points_totals

print("smart v dumb:")
print(dumb_v_smart)
print(" ")
print("smart v smarter")
print(smart_v_smarter)