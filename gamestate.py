# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 15:59:16 2018

@author: martin
"""

#from typing import NamedTuple
from collections import namedtuple
import constants as con
import copy

class GameState(namedtuple('GameState', ['game_mode', 'offensive_player',
                                         'active', "history", "player_points"])
                ):
    """

    Subclassing NamedTuple makes the states (effectively) immutable
    and hashable. Using immutable states can help avoid errors that
    can arise with in-place state updates. Hashable states allow the
    state to be used as the key to a look up table.
    
    history = "1H9_2E103HU_" is a single long string. each action played takes 
              up four characters. The first character denotes who played the 
              card, and the latter three specify which card was played. The
              underscores are to pad out card symbols sol that all have length 3. 
              A full round is four cards and is thus 16 characters long. 

    """
    def __new__(cls, game_mode="", offensive_player=None, active=None,
                history="", player_points = (0, 0, 0, 0)):
        if not game_mode in con.GAME_MODES:
            raise ValueError("{} is not a valid game mode".format(game_mode))
        if not (len(history) %4 == 0):
            raise ValueError("The inputted history is not correct.")

        return super(GameState, cls).__new__(cls, game_mode, offensive_player, active, history, player_points)

    # ------------------------ Helper Functions ----------------------------- #
    def get_current_round(self):
        start, junk = divmod(len(self.history), 16) # is 4*4
        return self.history[start * 16:]
    
    def get_round_number(self):
        round_num, _ = divmod(len(self.history), 16) # is 4*4
        return round_num

    def split_by_stride(self, input_string, stride = 4):
        ind = 0
        out = []
        while not ind >= len(input_string):
            out += [input_string[ind:ind+stride]]
            ind += stride
        return out
    
    def player_card_tuples(self, input_string):
        ind = 0
        out = []
        while not ind >= len(input_string):
            out += [(int(input_string[ind]), input_string[ind+1:ind+4])]
            ind += 4
        return out
    
    def partner_game(self):
        """ If the current game is a partner game, return True, else False ."""
        return self.game_mode in ["Partner Eichel", "Partner Schellen", "Partner Gras"]
    
    def played_the_ace(self):
        """ Returns the number of the player who played the called ace, if known
        
        Returns
        -------
        int
            Player number, if known. Else None.
        """
        if not self.partner_game():
            raise ValueError("{} is not a partner game".format(self.game_mode))
        
        suit = self.game_mode.split(" ")[1][0] # extract first letter of game_mode (FRAGILE!)
        ace = suit+"A_"
        for i in range(len(self.history) // 4): 
            if ace in self.history[i*4: (i+1)*4]:
                return int(self.history[i*4])
            
        return None
            
    # ----------------------------------------------------------------------- # 
        
    def actions(self, hand):
        """Get available actions for a player given his hand. This function
        can be somewhat hard to understand, given the many game types of 
        schafkopf. In short, if one is playing the opening move, 
        then they can play anything. If not, they must match the suit of the 
        card which was played. If they cannot, then they may play anything. 
        
        Except if one is playing a partner game, and he has the called ace. 
        Then he must play the called ace, if it's suit was played. It gets more
        complicated than this due to the technicality of "running away" or 
        "davonlaufen".
        
        Parameters
        ----------
        hand: iterable
            An Iterable of strings of the form AK_, S10 etc. 
        
        Returns
        -------
        list 
             a list of available cards to be played, as strings. """
        hand = list(hand)
        
        if len(hand) == 1:
            return hand   
        
        current_round = self.get_current_round()
        _, _, called_ace, suit_dictionary = con.constants_factory(self.game_mode)
        
        if current_round:
            current_suit = suit_dictionary[current_round[1:4]] 
        else:
            current_suit = None
        
        matching_cards = [card for card in hand if suit_dictionary[card] == current_suit]
        # If I can't match the suit, play whatever. Also works if I'm coming out, if current_suit is None.
        if not(matching_cards):
            matching_cards = hand
        
        # check if we're playing a partner game, and I have the called ace. 
        # If we're not doing partner play, called_ace is None
        if called_ace in hand: 
            called_colour = suit_dictionary[called_ace]
            if current_round:
                # Someone has played a card before me, I'm not coming out.
                if current_suit == called_colour:
                    # play the ace if I have it
                    return [called_ace]
                else: 
                    # play any valid card that isn't the ace
                    return [card  for card in matching_cards if card != called_ace]
                
            else: 
                # If i am allowed to come out.
                if len([card for card in hand if suit_dictionary[card] == called_colour]) >= 4:
                    # can "run away" and not open with the ace. 
                    return hand
                else:
                    # Can open with the called ace, but not any other card of the called colour
                    return [card  for card in hand if 
                            (card == called_ace) or (suit_dictionary[card] != called_colour)]  

        return matching_cards


    # -------------------------------------------------
    def result(self, action):
        """ Return the resulting game state after applying the action specified
        to the current game state.

        Note that players can choose any open cell on the opening move,
        but all later moves MUST be one of the values in Actions.

        Parameters
        ----------
        action : str
            A string indicating the card played by the active player.

        Returns
        -------
        GameState
            A new state object with the input move applied.
        """
        if not (action in con.ALL_CARDS):
            print(type(action))
            print(action)
            raise ValueError("{} is not a valid action.".format(action))
        
        new_history = self.history+str(self.active)+action
        game_mode = self.game_mode
        offensive_player = self.offensive_player
        if len(new_history) % 16 == 0:
            round_string = new_history[-16:]
            new_active, points = self.calculate_round_winner(round_string)
            player_points = tuple(p if i != new_active else p + points for i, p in enumerate(self.player_points))
        else:
            new_active = (self.active + 1) % 4
            player_points = self.player_points
        
        return GameState(history= new_history, active=new_active,
                         game_mode = game_mode, offensive_player=offensive_player,
                         player_points=player_points)
        
        
    def calculate_round_winner(self, round_string=None):
        """ Calculate the winner of the last round.
        Parameters
        ----------
        round_string : str
            A string of length 16 denoting the last round played.

        Returns
        -------
        winning_player
            An integer denoting the number of the playe who won. 
            
        points
            An integer denoting the number of points that the winning_player won.  
        
        """
        if round_string is None:
            round_string = self.history[-16:]
        if len(round_string) != 16:
            raise ValueError("Round has not been played to completion.")
            
        card_ordering, trump_ordering, called_ace, suit_dictionary = con.constants_factory(self.game_mode)
            
        readable = self.player_card_tuples(round_string)
        suit = suit_dictionary[round_string[1:4]] # suit of first card played

        trumps = [tup for tup in 
                  readable if suit_dictionary[tup[1]] == "Truempfe"]
 
        if trumps:
            winning_player =  sorted(trumps, key=lambda x:
                            trump_ordering.index(x[1]),reverse=True)[0][0]
            # extract the player number
        else:
            # If no trumps, the highest card matching the suit will win. 
            correct_suit_cards = [tup for tup in readable
                                  if suit_dictionary[tup[1]] == suit]
            winning_player = sorted(correct_suit_cards, key=lambda x:
                card_ordering.index(x[1][1:]), reverse=True)[0][0] 
            
        points = sum(con.POINTS[c] for p, c in readable)
        return int(winning_player), points
    # -------------------------------------------------   

    def terminal_test(self):
        """ Return True if 32 cards have been played, otherwise False

        Returns
        -------
        bool
            True if either player has no legal moves, otherwise False
        """
        if len(self.history) == 128: # is 32*4
            return True
        elif (len(self.history)) < 128:
            return False
        else:
            raise ValueError("Someone tried to play past the end of the game")
          
    
    def utilities(self):
        """ 
        Returns
        -------
        tuple
            A tuple containing the utility value of the current game state for 
            all players. The game has a utility of +1 if the player has won,
            a value of -1 if the player has lost, and a value of 0
            otherwise.
        """

        if not self.terminal_test():
            return (0, 0, 0, 0)
        
        if self.game_mode == "Ramsch":
            max_score = max(self.player_points)
            return tuple(-1 if p == max_score else 1 for p in self.player_points)
            # Also covers the case of a tie.
        elif self.partner_game():
            offensive_team = (self.offensive_player, self.played_the_ace())
        else:
            offensive_team = (self.offensive_player,)

        off_points = sum(self.player_points[i] for i in offensive_team)
        def_points = 120 - off_points        
        
        if off_points >= 61:
            return tuple(1 if i in offensive_team else -1 for i in range(4))
        else:
            return tuple(-1 if i in offensive_team else 1 for i in range(4))
        
    def utilities_test(self):
        """ 
        Testing if a different utility function improves my MCTS bots.
        """

        if not self.terminal_test():
            return (0, 0, 0, 0)
        
        if self.game_mode == "Ramsch":
            return tuple(-p for p in self.player_points)

        elif self.partner_game():
            offensive_team = (self.offensive_player, self.played_the_ace())
        else:
            offensive_team = (self.offensive_player,)

        off_points = sum(self.player_points[i] for i in offensive_team)
        def_points = 120 - off_points        
        
        return tuple(off_points if i in offensive_team else def_points for i in range(4))

        
        
    def __str__(self):
        outstring =  "============== New Game =============\n"
        if self.game_mode == "Ramsch":
            outstring += "The players played a Ramsch"
        else:
            outstring += "Player {} called a {}.".format(self.offensive_player, self.game_mode)
        outstring += "\n====================================="
        history = self.history
        for i in range(0, 8):
            line = history[i*16: (i+1)*16]
            things = self.player_card_tuples(line)
            line_str = ""
            for p_id, card in things:
                if card[2] == "_":
                    card = card[0:2]+" "
                line_str += "{} {}   ".format(p_id, card)
                
            outstring += "\nRound {}: ".format(i+1)+line_str
            
        if self.terminal_test():
            outstring += "\n====================================="
            utility = self.utilities()
            winners = [str(i) for i in range(4) if utility[i] == 1]
            losers = [str(i) for i in range(4) if utility[i] == -1]
            win_points = sum(self.player_points[int(i)] for i in winners)
            outstring += ("\nWinners: "+" ".join(winners)).ljust(16) +"Total points: {}".format(win_points)
            outstring += ("\nLosers : "+" ".join(losers)).ljust(16) +"Total points: {}".format(120 - win_points)
            outstring += "\n====================================="
            
        return outstring
