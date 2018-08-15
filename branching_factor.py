# -*- coding: utf-8 -*-
"""
Small script to find the average branching factor at each ply of the game. 
No other programs depend on this. 
"""

from environments import Arena
import matplotlib.pyplot as plt
import numpy as np

sum_branches = {i:0 for i in range(32)}


class NewArena(Arena):
    def play_game(self, state, verbose):
        """ Takes a prepared game_state object and plays rounds to completion.
        Is overridden in the human interface class."""
        for i in range(32):
            active = state.active
            n_options = len(state.actions(self.agents[active].hand))
            card = self.agents[active].play_card(state)
            sum_branches[i] += n_options
            state = state.result(card)
        
        game_points = self.winner_game_points(state.utilities())
        for i in range(4):
            self.points_totals[i] += game_points[i]
        if verbose:
            print(state)
        # update points totals.



bots_list = ["DUMB", "DUMB", "DUMB", "DUMB"]

arena = NewArena(bots_list)
n_matches = 10000

for i in range(n_matches):
    arena.new_game(verbose = False)
    
    
average_branching = {i: n/n_matches for i,n in sum_branches.items()}

y = list(average_branching.values())
plt.figure()
plt.plot(y)
plt.xlabel("Ply number")
plt.ylabel("Branching factor")

new_y = [y[0]]
for i in range(1,len(y)):
    new_y += [y[i]*new_y[i-1]]
    
plt.figure()
plt.plot(np.log(new_y))
plt.xlabel("Ply number")
plt.ylabel("log Branching factor")



