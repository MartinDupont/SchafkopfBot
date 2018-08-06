# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:48:20 2018

@author: martin
"""

from environments import Arena

botstring = ["MCTS", "MCTSPLUS", "DUMB", "DUMB"]
#botstring = ["MCTS", "DUMB", "DUMB", "DUMB"]
#botstring = ["MCTSPLUS", "MCTSPLUS", "MCTSPLUS", "MCTSPLUS" ]

arena = Arena(botstring)

for i in range(500):
    arena.new_game(verbose = False)

    print("Round end total points:")  
    print(arena.points_totals)
    
 
dumb_v_smart = arena.points_totals
    
botstring = ["MCTSPLUS", "MCTSPLUS", "MCTS", "MCTS" ]


for i in range(250):
    arena.new_game(verbose = False)

    print("Round end total points:")  
    print(arena.points_totals)
    
smart_v_smarter = arena.points_totals

print("smart v dumb:")
print(dumb_v_smart)
print(" ")
print("smart v smarter")
print(smart_v_smarter)