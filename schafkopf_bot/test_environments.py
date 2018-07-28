# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 22:31:45 2018

@author: martin
"""

import unittest
from bots import DumbBot
from environments import Arena

class CheckArena(unittest.TestCase):
    def test_play_full_game(self):
        bots_list = ["DUMB", "DUMB", "DUMB", "DUMB"]
        arena = Arena(bots_list, 1)
        for _ in range(10):
            arena.new_game()
            
            
if __name__ == "__main__":
    unittest.main()