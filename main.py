# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 22:17:07 2018

@author: martin
"""
import sys

#print(sys.path)
#import constants.constants as con

#print(con.ALL_CARDS)

from bots.thing import Thing

from bots import DumbBot, BaseBot, HeuristicBot, MonteCarloBot

from nodes import Node

bot = MonteCarloBot()

hand = ["EA_", "EK_", "E10", "E9_", "E8_", "S7_", "EU_", "EO_"]

bot.hand = hand
print(bot.play_or_not())