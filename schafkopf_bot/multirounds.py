# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:48:20 2018

@author: martin
"""

from environments import Arena

botstring = ["MCTS", "MCTS", "DUMB", "DUMB"]

arena = Arena(botstring)

for i in range(20):
    arena.new_game()

print("Round end total points:")  
print(arena.points_totals)