# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 15:59:16 2018

@author: martin
"""

#from typing import NamedTuple
from collections import namedtuple
import constants as con

class GameState():
    """ This is just a factory which returns the different gamestates for 
    a given gamemode. It's a bit hacky, in that it never returns a GameState
    object. I'm not sure if it's a great approach."""
    def __new__(cls, game_mode="", offensive_player=None, active=None,
                history="", player_points = (0, 0, 0, 0)):
        
        if not game_mode in con.GAME_MODES:
            raise ValueError("{} is not a valid game mode".format(game_mode))
            
        if game_mode == "Ramsch":
            return RamschState(game_mode, offensive_player, active, history, player_points) 
        elif game_mode in ["Partner Gras", "Partner Eichel", "Partner Schellen"]:
            return PartnerState(game_mode, offensive_player, active, history, player_points) 
        elif game_mode in ["Herz Solo", "Eichel Solo", "Gras Solo", "Schellen Solo", "Wenz"]:
            return SoloState(game_mode, offensive_player, active, history, player_points) 


class BaseState(namedtuple('GameState', ['game_mode', 'offensive_player',
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

        return super(BaseState, cls).__new__(cls, game_mode, offensive_player, active, history, player_points)

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
            winning_player =  max(trumps, key=lambda x:
                            trump_ordering.index(x[1]))[0]
            # extract the player number
        else:
            # If no trumps, the highest card matching the suit will win. 
            correct_suit_cards = [tup for tup in readable
                                  if suit_dictionary[tup[1]] == suit]
            winning_player = max(correct_suit_cards, key=lambda x:
                card_ordering.index(x[1][1:]))[0] 
            
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
          
    def tally_points(self):
        """ Counts points accumulated by each player so far, including points
        scored by teammates, if they exist.
        Returns
        -------
        tuple
            A tuple of the points each player has accrued."""
        raise NotImplementedError
        
    def is_decided(self):
        """ In schafkopf, a game may be decided before the game is over. Note,
        that this does not immediately end the game, as it is the responsibility
        of the players to keep count of the points. In addition, a bigger 
        prize is awarded for winning by over 90 points, so players have an 
        incentive to keep playing after they know the game is over.
        
        Returns
        -------
            bool  """
        utils = self.utilities(bools=True, intermediate=True)
        if not utils == (0, 0, 0, 0):
            return True
        return False
    
    def utilities(self, bools=True, intermediate=False):
        """ Calculates the expected utility for each player. There are various
        ways of potentially calculating utility.
        Parameters
        ----------
        bools : boolean
            If True, returns a tuple of 1's and zeros, corresponding to whether
            a player won or lost the game, ignoring how much they won the game by.
            If False, it will return a utility proportional to how many points
            the player has won, including points potentially won by his teammates.
            Values of the tuple will be in [0, 120]
            
        intermediate: boolean
            controls whether to evaluate utility at intermediate stages of the
            game. For example, sometimes the outcome is known before the game
            is over and so a state has a utility associated with it. 
            If True and bools is true, it will deliver a tuple of 1's and 0's 
            if the outcome is already known, and a tuple of 0's if the outcome 
            is still unknown. 
            
            If True and bools is False, then it will deliver the result of 
            the tally-points function, unless we are in a Ramsch, then it will
            deliver 120 minus those points, to account for the fact that more
            points in a ramsch are worse. 
        
        Returns
        -------
        tuple
            A tuple containing the utility value of the current game state for 
            all players. The game has a utility of +1 if the player has won,
            a value of -1 if the player has lost, and a value of 0
            otherwise.
        """
        raise NotImplementedError

                
    def __str__(self):
        outstring =  "================ Game ===============\n"
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
            losers = [str(i) for i in range(4) if utility[i] == 0]
            win_points = sum(self.player_points[int(i)] for i in winners)
            outstring += ("\nWinners: "+" ".join(winners)).ljust(16) +"Total points: {}".format(win_points)
            outstring += ("\nLosers : "+" ".join(losers)).ljust(16) +"Total points: {}".format(120 - win_points)
            outstring += "\n====================================="
            
        return outstring

# =========================================================================== #
#                          Specific Game Modes
# =========================================================================== #


class RamschState(BaseState):
    def __new__(cls, game_mode="", offensive_player=None, active=None,
                history="", player_points = (0, 0, 0, 0)):
        if not game_mode == "Ramsch":
            raise ValueError("{} is not 'Ramsch'. Something went wrong with initialization".format(game_mode))
        if not (len(history) %4 == 0):
            raise ValueError("The inputted history is not correct.")

        return super(RamschState, cls).__new__(cls, game_mode, offensive_player, active, history, player_points) 
    
    
    def tally_points(self):
        return self.player_points
    
    def utilities(self, bools=True, intermediate=False):
        if (intermediate is False) and not(self.terminal_test()):
            return (0, 0, 0, 0)
        
        points_tally = self.player_points
        if not bools:
            return tuple(120 - p for p in points_tally)
        # if we are returning a non-boolean utility, then the calculation
        # doesn't change if we are in an intermediate state or not. 
        # Must return 120 minus points, because in a ramsch, having more points
        # is BAD. Other agents will often want to normalize the points utility
        # by dividing by 120, to keep the utility in [0,1]. Returning 120-p 
        # ensures that for ALL gamestates, we can normalize by dividing by 120.
        
        remaining = 120 - sum(self.player_points)
        rank = sorted(self.player_points, reverse=True)
        first, second = rank[0], rank[1]
            
        if (remaining == 0) or (first - second > remaining):
            return tuple(0 if points_tally[i] == first else 1 for i in range(4))
            # Either the game is over, or one player has so many points that 
            # nobody can catch up. 
        return (0, 0, 0, 0)
        # outcome is still unknown. 

            
    

class PartnerState(BaseState):
    def __new__(cls, game_mode="", offensive_player=None, active=None,
                history="", player_points = (0, 0, 0, 0)):
        if not game_mode in ["Partner Eichel", "Partner Gras", "Partner Schellen"]:
            raise ValueError("{} is not a partner game. Something went wrong with initialization".format(game_mode))
        if not (len(history) %4 == 0):
            raise ValueError("The inputted history is not correct.")

        return super(PartnerState, cls).__new__(cls, game_mode, offensive_player, active, history, player_points) 

    def tally_points(self):
        partner = self.played_the_ace()
        if not partner is None:
            offensive_team = (self.offensive_player, partner)
            defensive_team = tuple(i for i in range(4) if not i in offensive_team)
            off_points = sum(self.player_points[i] for i in offensive_team)
            def_points = sum(self.player_points[i] for i in defensive_team)
            
            points_tally = tuple(off_points if i in offensive_team else def_points for i in range(4))
        else:
            points_tally = self.player_points
            # Nobody knows their partner yet (for sure), so we can't combine points
        
        return points_tally 
            # Nobody knows their partner yet (for sure), so we can't combine points

    def utilities(self, bools=True, intermediate=False):
        if (intermediate is False) and not(self.terminal_test()):
            return (0, 0, 0, 0)
        
        points_tally = self.tally_points()
        if not bools:
            return points_tally
        
        partner = self.played_the_ace()
        offensive = self.offensive_player
        if partner is None:
            # We don't know winners, because we don't know who's playing with who.
            return (0, 0, 0, 0)
        else:
            offensive_team = (offensive, partner)
            defensive_team = tuple(i for i in range(4) if not i in offensive_team)
            
            off_points = points_tally[offensive]
            def_points = points_tally[defensive_team[0]]
            if off_points >= 61:
                return tuple(1 if i in offensive_team else 0 for i in range(4))
            if def_points >= 60:
                return tuple(1 if i in defensive_team else 0 for i in range(4))
            return (0, 0, 0, 0)
        
        

    def actions(self, hand):
        """ Overrides actions from base game to acommodate playing the called ace.  
        
        If one is playing a partner game, and he has the called ace. 
        Then he must play the called ace, if it's suit was played. There is 
        also the special case of "running away" or "davonlaufen"; if a player
        who has the called ace has four or more cards of that same colour in 
        his hand, then he may open with one of those cards instead of the ace."""
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




class SoloState(BaseState):
    def __new__(cls, game_mode="", offensive_player=None, active=None,
                history="", player_points = (0, 0, 0, 0)):
        if not game_mode in ["Herz Solo", "Eichel Solo", "Schellen Solo", "Gras Solo", "Wenz"]:
            raise ValueError("{} is not a solo game. Something went wrong with initialization".format(game_mode))
        if not (len(history) %4 == 0):
            raise ValueError("The inputted history is not correct.")

        return super(SoloState, cls).__new__(cls, game_mode, offensive_player, active, history, player_points)    


    def tally_points(self):
        
        offensive = self.offensive_player
        defensive = tuple(i for i in range(4) if not i == offensive)
        
        off_points = self.player_points[offensive]
        def_points = sum(self.player_points[i] for i in defensive)
        
        points_tally = tuple(off_points if i == offensive else def_points for i in range(4))
        
        return points_tally
    
    def utilities(self, bools=True, intermediate=False):
        if (intermediate is False) and not(self.terminal_test()):
            return (0, 0, 0, 0)
        
        points_tally = self.tally_points()
        if not bools:
            return points_tally
        
        offensive = self.offensive_player
        defensive = tuple(i for i in range(4) if not i == offensive)[0] 
        # only need one defensive player, because the points were aggregated earlier. 
        if points_tally[offensive] >= 61:
            return tuple(1 if i == offensive else 0 for i in range(4))
        elif points_tally[defensive] >= 60:
            return tuple(1 if i != offensive else 0 for i in range(4))
        else:
            return (0, 0, 0, 0)

