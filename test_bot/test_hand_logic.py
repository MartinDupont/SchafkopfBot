# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 17:28:46 2018

@author: martin
"""

import unittest

from context import schafkopf_bot as sb

class CheckDavonlaufen(unittest.TestCase):
    def setUp(self):
        self.bot = sb.DumbBot()
        self.bot.gamemode = "normale Eichel"
        self.bot.hand = ["E7","E8", "E9" ,"EA","S7"]
    
    def test_open_davonlaufen(self):
        self.bot.played_so_far = []
        allowed = self.bot.calculate_legal_moves()
        self.assertEqual(allowed, self.bot.hand)
        
    def test_follow(self):
        self.bot.played_so_far = ["E10"]
        allowed = self.bot.calculate_legal_moves()
        expected = ["EA"]
        self.assertEqual(allowed, expected)
        
    def test_open_normal(self):
        self.bot.hand.remove("E9")
        self.bot.played_so_far = []
        allowed = self.bot.calculate_legal_moves()
        expected = ["EA","S7"]
        self.assertEqual(allowed, expected)
    
    def test_follow_not_called(self):
        self.bot.playedThisRound = ["G10"]
        self.bot.currentSuit = "Gras"
        allowed = self.bot.calculateLegalMoves()
        expected = ["E7","E8", "E9" ,"S7"]
        self.assertEqual(allowed, expected)
        
        
if __name__ == "__main__":
    unittest.main()