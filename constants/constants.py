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
              'Eichel'  : ('E7_', 'E8_', 'E9_', 'E10', 'EK_', 'EA_', 'EO_'),
              'Herz'    : ('H7_', 'H8_', 'H9_', 'H10', 'HK_', 'HA_', 'HO_'),
              'Truempfe': ('HU_', 'SU_', 'GU_', 'EU_')}

GRAS_SOLO_SUITS = {'Schellen': ('S7_', 'S8_', 'S9_', 'S10', 'SK_', 'SA_'),
                   'Truempfe': ('G7_', 'G8_', 'G9_', 'G10', 'GK_', 'GA_', 'HU_', 
                                'HO_', 'SU_', 'SO_', 'GU_', 'GO_', 'EU_', 'EO_'),
                   'Eichel'  : ('E7_', 'E8_', 'E9_', 'E10', 'EK_', 'EA_'),
                   'Herz'    : ('H7_', 'H8_', 'H9_', 'H10', 'HK_', 'HA_')}

SCHELLEN_SOLO_SUITS = {'Truempfe': ('S7_', 'S8_', 'S9_', 'S10', 'SK_', 'SA_', 'HU_',
                                    'HO_', 'SU_', 'SO_', 'GU_', 'GO_', 'EU_', 'EO_'),
                       'Gras'    : ('G7_', 'G8_', 'G9_', 'G10', 'GK_', 'GA_'),
                       'Eichel'  : ('E7_', 'E8_', 'E9_', 'E10', 'EK_', 'EA_'),
                       'Herz'    : ('H7_', 'H8_', 'H9_', 'H10', 'HK_', 'HA_')}

EICHEL_SOLO_SUITS = {'Schellen': ('S7_', 'S8_', 'S9_', 'S10', 'SK_', 'SA_'),
                     'Gras'    : ('G7_', 'G8_', 'G9_', 'G10', 'GK_', 'GA_'),
                     'Truempfe': ('E7_', 'E8_', 'E9_', 'E10', 'EK_', 'EA_', 'HU_',
                                  'HO_', 'SU_', 'SO_',  'GU_', 'GO_', 'EU_', 'EO_'),
                     'Herz'    : ('H7_', 'H8_', 'H9_', 'H10', 'HK_', 'HA_')}

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


GAME_PRIORITY = {'Herz Solo': 3, 'Gras Solo': 3, 'Eichel Solo': 3,
                 'Schellen Solo': 3, 'Wenz': 2, 'Partner Schellen': 1,
                 'Partner Eichel': 1, 'Partner Gras': 1,
                 "Ramsch": 0, None: float("-inf")}

NORMAL_ORDERING = ('7_', '8_', '9_', 'K_', '10', 'A_')
WENZ_ORDERING = ('7_', '8_', '9_', 'O_', 'K_', '10', 'A_')

# ============== Trump Ordering for all game modes ========================== #
NORMAL_TRUMP_ORDERING   = ('H7_', 'H8_', 'H9_', 'HK_', 'H10', 'HA_', 'SU_', 'HU_' ,
                           'GU_', 'EU_', 'SO_', 'HO_', 'GO_', 'EO_')
WENZ_TRUMP_ORDERING     = ('SU_', 'HU_', 'GU_', 'EU_')
GRAS_TRUMP_ORDERING     = ('G7_', 'G8_', 'G9_', 'GK_', 'G10', 'GA_', 'SU_', 'HU_',
                           'GU_', 'EU_', 'SO_', 'HO_', 'GO_', 'EO_')
EICHEL_TRUMP_ORDERING   = ('E7_', 'E8_', 'E9_', 'EK_', 'E10', 'EA_', 'SU_', 'HU_',
                           'GU_', 'EU_', 'SO_', 'HO_', 'GO_', 'EO_')
SCHELLEN_TRUMP_ORDERING = ('S7_', 'S8_', 'S9_', 'SK_', 'S10', 'SA_', 'SU_', 'HU_',
                           'GU_', 'EU_', 'SO_', 'HO_', 'GO_', 'EO_')

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


POINTS_REORDERED = {0 : ['S7_', 'S8_', 'S9_', 'G7_', 'G8_', 'G9_', 'H7_' ,'H8_' ,'H9_' ,
                         'E7_', 'E8_', 'E9_'],
                    11: ['SA_', 'GA_', 'HA_', 'EA_'],
                    10: ['S10', 'G10', 'H10', 'E10'],
                    4 : ['SK_', 'GK_', 'HK_', 'EK_'],
                    3 : ['SO_', 'GO_', 'HO_', 'EO_'],
                    2 : ['SU_', 'GU_', 'HU_', 'EU_']}

POINTS = reorder_dict(POINTS_REORDERED)

# ====================== Categories of Cards ================================ #
OBERS            = ["SO_", "HO_", "GO_", "EO_"]
UNTERS           = ["SU_", "HU_", "GU_", "EU_"]
EICHEL_SPATZEN   = ["E7_", "E8_", "E9_"]
GRAS_SPATZEN     = ["G7_", "G8_", "G9_"]
HERZ_SPATZEN     = ["H7_", "H8_", "H9_"]
SCHELLEN_SPATZEN = ["S7_", "S8_", "S9_"]

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

# ========================== Abstract Factories ============================= #

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

def get_categories(game_mode):
    if game_mode == "Wenz":
        return [UNTERS,
                EICHEL_SPATZEN,
                GRAS_SPATZEN,
                HERZ_SPATZEN,
                SCHELLEN_SPATZEN]
    return [OBERS, 
            UNTERS,
            EICHEL_SPATZEN,
            GRAS_SPATZEN,
            HERZ_SPATZEN,
            SCHELLEN_SPATZEN]


def make_play_order(i):
    return [(i + j) % 4 for j in range(4)]
    
    