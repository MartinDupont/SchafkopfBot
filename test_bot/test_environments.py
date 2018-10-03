# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 22:31:45 2018

@author: martin
"""

import unittest
from environments import Arena
from constants import constants as con

class CheckArena(unittest.TestCase):
    def setUp(self):
        self.bots_list = ["DUMB", "DUMB", "DUMB", "DUMB"]
        self.arena = Arena(self.bots_list)
    
    def test_deal_cards(self):
        """ The arena should deal 8 unique cards to four players? """
        initial_hands = {i: self.arena.agents[i].hand for i in range(4)}
        expected = {0: [], 1: [], 2: [], 3: []}        
        
        self.assertEqual(initial_hands, expected)
        
        self.arena.deal_cards()
        
        final_hands = {i: self.arena.agents[i].hand for i in range(4)}
        final_hand_lengths = {i: len(hand) for i, hand in final_hands.items()}
        
        expected = {0: 8, 1: 8, 2: 8, 3: 8}
        self.assertEqual(expected, final_hand_lengths)
        
        cards_dealt = set()
        for hand in final_hands.values():
            cards_dealt.update(hand)
  
        self.assertEqual(cards_dealt, set(con.ALL_CARDS))
        
    def test_who_will_play(self):
        """ It should ask each player in order if they want to play or not,
        delivering a true or false answer for each."""
        self.arena.deal_cards()
        
        who_will_play = self.arena.who_will_play()
        self.assertEqual(len(who_will_play), 4)
        
        true_false = {True, False}
        players = [x[0] for x in who_will_play]
        answers = [x[1] for x in who_will_play]
        
        self.assertTrue(set(answers).issubset(true_false))
        self.assertEqual(players, [0, 1, 2, 3])
        
    def test_winner_game_points_1(self):
        """ Does the arena correctly assign points to winning players? """
        result = self.arena.winner_game_points((1, 0, 0, 0))
        expected = (3, -1, -1, -1)
        
        self.assertEqual(result, expected)

    def test_winner_game_points_2(self):
        """ Does the arena correctly assign points to winning players? """
        result = self.arena.winner_game_points((1, 1, 0, 0))
        expected = (1, 1, -1, -1)
        
        self.assertEqual(result, expected)
    def test_winner_game_points_3(self):
        """ Does the arena correctly assign points to winning players? """
        result = self.arena.winner_game_points((0, 1, 1, 1))
        expected = (-3, 1, 1, 1)
        
        self.assertEqual(result, expected)        
    
    def test_play_full_game(self):
        """ The arena should be able to play a full game to completion. """
        self.arena.new_game(verbose=True)
            
        
    def test_increment_active_player(self):
        """ The arena should correctly rotate the starting player. """
        arena = Arena(self.bots_list, 1)
        
        self.assertEqual(arena.comes_out, 1)
        arena.new_game(verbose=True)
        self.assertEqual(arena.comes_out, 2)
           
    def test_zero_sum_points(self):
        """ The points assigned to each player should be zero-sum. """

        for _ in range(10):
            self.arena.new_game(verbose=True)
            
        total = sum(self.arena.points_totals.values())
        self.assertEqual(total, 0)
            
if __name__ == "__main__":
    unittest.main()