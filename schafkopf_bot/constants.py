# -*- coding: utf-8 -*-
"""
All constants used for the schafkopf robot. Specifies which cards are in play,
and which cards belong to which suits etc. for the different game modes. 
"""
import numpy as np

def reorder_dict(dic):
    out = {}
    for d in dic:
        for a in dic[d]:
            out[a] = d
    return out


# ============================ Basic Stuff ================================== #
    
ALL_CARDS = ['S7_', 'S8_', 'S9_', 'S10', 'SK_', 'SA_', 'SU_', 'SO_',
             'H7_', 'H8_', 'H9_', 'H10', 'HK_', 'HA_', 'HU_', 'HO_',
             'G7_', 'G8_', 'G9_', 'G10', 'GK_', 'GA_', 'GU_', 'GO_',
             'E7_', 'E8_', 'E9_', 'E10', 'EK_', 'EA_', 'EU_', 'EO_']

GAME_MODES = ['Ramsch', 'Herz Solo', 'Schellen Solo', 'Eichel Solo',
              'Gras Solo', 'Wenz', 'Partner Schellen', 'Partner Eichel',
              'Partner Gras']

# ================= Suit Classification for all Game Modes ================== #

STANDARD_SUITS = {'Schellen': ('S7_', 'S8_', 'S9_', 'S10', 'SK_', 'SA_'),
                  'Gras'    : ('G7_', 'G8_', 'G9_', 'G10', 'GK_', 'GA_'),
                  'Eichel'  : ('E7_', 'E8_', 'E9_', 'E10', 'EK_', 'EA_'),
                  'Truempfe': ('H7_', 'H8_', 'H9_', 'H10', 'HK_', 'HA_',
                               'HU_', 'HO_', 'SU_', 'SO_', 'GU_', 'GO_',
                               'EU_', 'EO_')}
                
WENZ_SUITS = {'Schellen': ('S7_', 'S8_', 'S9_', 'S10', 'SK_', 'SA_', 'SO_'),
              'Gras'    : ('G7_', 'G8_', 'G9_', 'G10', 'GK_', 'GA_', 'GO_'),
              'Eichel'  : ('E7', 'E8', 'E9', 'E10', 'EK', 'EA', 'EO'),
              'Herz'    : ('H7', 'H8', 'H9', 'H10', 'HK', 'HA', 'HO'),
              'Truempfe': ('HU', 'SU', 'GU', 'EU')}

GRAS_SOLO_SUITS = {'Schellen': ('S7', 'S8', 'S9', 'S10', 'SK', 'SA'),
                   'Truempfe': ('G7', 'G8', 'G9', 'G10', 'GK', 'GA', 'HU', 
                                'HO', 'SU', 'SO', 'GU', 'GO', 'EU', 'EO'),
                   'Eichel'  : ('E7', 'E8', 'E9', 'E10', 'EK', 'EA'),
                   'Herz'    : ('H7', 'H8', 'H9', 'H10', 'HK', 'HA')}

SCHELLEN_SOLO_SUITS = {'Truempfe': ('S7', 'S8', 'S9', 'S10', 'SK', 'SA', 'HU',
                                    'HO', 'SU', 'SO', 'GU', 'GO', 'EU', 'EO'),
                       'Gras'    : ('G7', 'G8', 'G9', 'G10', 'GK', 'GA'),
                       'Eichel'  : ('E7', 'E8', 'E9', 'E10', 'EK', 'EA'),
                       'Herz'    : ('H7', 'H8', 'H9', 'H10', 'HK', 'HA')}

EICHEL_SOLO_SUITS = {'Schellen': ('S7', 'S8', 'S9', 'S10', 'SK', 'SA'),
                     'Gras'    : ('G7', 'G8', 'G9', 'G10', 'GK', 'GA'),
                     'Truempfe': ('E7', 'E8', 'E9', 'E10', 'EK', 'EA', 'HU',
                                  'HO', 'SU', 'SO',  'GU', 'GO', 'EU', 'EO'),
                     'Herz'    : ('H7', 'H8', 'H9', 'H10', 'HK', 'HA')}

STANDARD_MAPPING = reorder_dict(STANDARD_SUITS)


        
SUITS_MAPPING = {'Wenz'            : reorder_dict(WENZ_SUITS),
                 'Herz Solo'       : STANDARD_MAPPING,
                 'Gras Solo'       : reorder_dict(GRAS_SOLO_SUITS),
                 'Eichel Solo'     : reorder_dict(EICHEL_SOLO_SUITS),
                 'Schellen Solo'   : reorder_dict(SCHELLEN_SOLO_SUITS),
                 'Partner Schellen': STANDARD_MAPPING,
                 'Partner Gras'    : STANDARD_MAPPING,
                 'Partner Eichel'  : STANDARD_MAPPING,
                 'Ramsch'          : STANDARD_MAPPING}
 
# ========================== Miscellaneous ================================== #
       
GAME_MODE_TO_ACES = {'Partner Schellen': 'SA_', 'Partner Eichel': 'EA_',
                     'Partner Gras': 'GA_'}


GAME_PRIORITY = {'Herz Solo': 1, 'Gras Solo': 1, 'Eichel Solo': 1,
                 'Schellen Solo': 1, 'Wenz': 2, 'Partner Schellen': 3,
                 'Partner Eichel': 3, 'Partner Gras': 3}

NORMAL_ORDERING = ('7', '8', '9', 'K', '10', 'A')
WENZ_ORDERING = ('7', '8', '9', 'O', 'K', '10', 'A')

# ============== Trump Ordering for all game modes ========================== #
NORMAL_TRUMP_ORDERING   = ('H7', 'H8', 'H9', 'HK', 'H10', 'HA', 'SU', 'HU' ,
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO')
WENZ_TRUMP_ORDERING     = ('SU', 'HU', 'GU', 'EU')
GRAS_TRUMP_ORDERING     = ('G7', 'G8', 'G9', 'GK', 'G10', 'GA', 'SU', 'HU',
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO')
EICHEL_TRUMP_ORDERING   = ('E7', 'E8', 'E9', 'EK', 'E10', 'EA', 'SU', 'HU',
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO')
SCHELLEN_TRUMP_ORDERING = ('S7', 'S8', 'S9', 'SK', 'S10', 'SA', 'SU', 'HU',
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO')

TRUMP_ORDERINGS = {'Wenz'            : WENZ_TRUMP_ORDERING,
                   'Herz Solo'       : NORMAL_TRUMP_ORDERING,
                   'Gras Solo'       : GRAS_TRUMP_ORDERING,
                   'Eichel Solo'     : EICHEL_TRUMP_ORDERING,
                   'Schellen Solo'   : SCHELLEN_TRUMP_ORDERING,
                   'Ramsch'          : NORMAL_TRUMP_ORDERING,
                   'Partner Schellen': NORMAL_TRUMP_ORDERING,
                   'Partner Gras'    : NORMAL_TRUMP_ORDERING,
                   'Partner Eichel'  : NORMAL_TRUMP_ORDERING}

# ============================ Points ======================================= #


POINTS_REORDERED = {0 : ['S7', 'S8', 'S9', 'G7', 'G8', 'G9', 'H7' ,'H8' ,'H9' ,
                         'E7', 'E8', 'E9'],
                    11: ['SA', 'GA', 'HA', 'EA'],
                    10: ['S10', 'G10', 'H10', 'E10'],
                    4 : ['SK', 'GK', 'HK', 'EK'],
                    3 : ['SO', 'GO', 'HO', 'EO'],
                    2 : ['SU', 'GU', 'HU', 'EU']}

POINTS = reorder_dict(POINTS_REORDERED)
# ====================== Card-Vector Translation ============================ #

card_vec_dict = {card: i for i, card in enumerate(ALL_CARDS)}
vec_card_dict = {i: card for i, card in enumerate(ALL_CARDS)}

def cards_2_vec(card_list):
    out = np.zeros(32, dtype=int)
    for c in card_list:
        index = card_vec_dict[c]
        out[index] = 1
    return out
    
def vec_2_cards(vector):
    out = []
    nonzero = np.where(vector)[0]
    for i in nonzero:
        out += [vec_card_dict[i]]
    return out

# ========================== Abstract Factory =============================== #

def constants_factory(game_mode):
    """Different game modes will have different trump cards, different suits,
    and different orderings. This function yields the correct constants 
    for a given game."""
    
    if game_mode == "Wenz":
        card_ordering = WENZ_ORDERING
    else:
        card_ordering = NORMAL_ORDERING
        
    trump_ordering = TRUMP_ORDERINGS[game_mode]
    
    try:
        called_ace = GAME_MODE_TO_ACES[game_mode]
    except KeyError:
        called_ace = None

    suit_dictionary = SUITS_MAPPING[game_mode]
    
    return card_ordering, trump_ordering, called_ace, suit_dictionary


def make_play_order(i):
    return [(i + j) % 4 for j in range(4)]
    
    