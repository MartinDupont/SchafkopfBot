# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 22:55:50 2018

@author: martin
"""


environment = HumanInterface()

while True:
    environment.new_game()
    for i in range(8):
        environment.play_round()
    environment.calculate_winner()
    
    