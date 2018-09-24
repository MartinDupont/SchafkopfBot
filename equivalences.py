# -*- coding: utf-8 -*-
"""
Small script to find the reduction in average branching factor at each ply 
of the game, after filtering out equivalent cards.  
No other programs depend on this. 
"""

from environments import Arena
import matplotlib.pyplot as plt
import numpy as np
from card_counting import filter_equivalent_cards

sum_branches = {i:0 for i in range(32)}
sum_branches_after = {i:0 for i in range(32)}

class NewArena(Arena):
    def play_game(self, state, verbose):
        """ Takes a prepared game_state object and plays rounds to completion.
        Is overridden in the human interface class."""
        for i in range(32):
            active = state.active
            n_options = len(state.actions(self.agents[active].hand))
            n_options_after = len(filter_equivalent_cards(state, state.actions(self.agents[active].hand)))
            card = self.agents[active].play_card(state)
            sum_branches[i] += n_options
            sum_branches_after[i] += n_options_after
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
    
    
average_branching = np.array([sum_branches[n]/n_matches for n in range(32)])
average_branching_after = np.array([sum_branches_after[n]/n_matches for n in range(32)])

plt.figure()
plt.plot(average_branching, label ="average before filtering")
plt.plot(average_branching_after, label="average after filtering")
plt.xlabel("Ply number")
plt.ylabel(" factor")
plt.legend()

#new_y = [y[0]]
#for i in range(1, len(y)):
#    new_y += [y[i] * new_y[i-1]]
#    
ratio = average_branching_after/ average_branching

plt.figure()
plt.plot(ratio)
#plt.xlabel("Ply number")
#plt.ylabel("log Branching factor")

difference = average_branching - average_branching_after

plt.figure()
plt.plot(difference)
#plt.xlabel("Ply number")
#plt.ylabel("log Branching factor")



