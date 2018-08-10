# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 20:18:17 2018

@author: martin
"""

gamemode = "Gras Solo"
hand = ["GK_", "HU_", "H7_" ,"H8_","G7_", "S7_", "G7_", "S9_"]
state = GameState(game_mode = gamemode, offensive_player = 2, active=3)

bot = MonteCarloPlus()

bot.hand = hand

#state = state.result()