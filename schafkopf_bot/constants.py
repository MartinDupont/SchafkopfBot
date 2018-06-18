# -*- coding: utf-8 -*-
"""
All constants used for the schafkopf robot. Specifies which cards are in play,
and which cards belong to which suits etc. for the different game modes. 
"""

def reorder_dict(dic):
    out = {}
    for d in dic:
        for a in dic[d]:
            out[a] = d
    return out


# ============================ Basic Stuff ================================== #
    
ALL_CARDS = ['S7', 'S8', 'S9', 'S10', 'SK', 'SA', 'SU', 'SO',
             'H7', 'H8', 'H9', 'H10', 'HK', 'HA', 'HU', 'HO',
             'G7', 'G8', 'G9', 'G10', 'GK', 'GA', 'GU', 'GO',
             'E7', 'E8', 'E9', 'E10', 'EK', 'EA', 'EU', 'EO']

GAME_MODES = ['Ramsch', 'Herz Solo', 'Schellen Solo', 'Eichel Solo',
              'Gras Solo', 'Wenz', 'Normale Schellen', 'Normale Eichel',
              'Normale Gras']

# ================= Suit Classification for all Game Modes ================== #

STANDARD_SUITS = {'Schellen': ['S7', 'S8', 'S9', 'S10', 'SK', 'SA'],
                  'Gras'    : ['G7', 'G8', 'G9', 'G10', 'GK', 'GA'],
                  'Eichel'  : ['E7', 'E8', 'E9', 'E10', 'EK', 'EA'],
                  'Truempfe': ['H7', 'H8', 'H9', 'H10', 'HK', 'HA', 'HU', 'HO',
                              'SU', 'SO', 'GU', 'GO', 'EU', 'EO']}
                
WENZ_SUITS = {'Schellen': ['S7', 'S8', 'S9', 'S10', 'SK', 'SA', 'SO'],
              'Gras'    : ['G7', 'G8', 'G9', 'G10', 'GK', 'GA', 'GO'],
              'Eichel'  : ['E7', 'E8', 'E9', 'E10', 'EK', 'EA', 'EO'],
              'Herz'    : ['H7', 'H8', 'H9', 'H10', 'HK', 'HA', 'HO'],
              'Truempfe': ['HU', 'SU', 'GU', 'EU']}

GRAS_SOLO_SUITS = {'Schellen': ['S7', 'S8', 'S9', 'S10', 'SK', 'SA'],
                   'Truempfe': ['G7', 'G8', 'G9', 'G10', 'GK', 'GA', 'HU', 
                                'HO', 'SU', 'SO', 'GU', 'GO', 'EU', 'EO'],
                   'Eichel'  : ['E7', 'E8', 'E9', 'E10', 'EK', 'EA'],
                   'Herz'    : ['H7', 'H8', 'H9', 'H10', 'HK', 'HA']}

SCHELLEN_SOLO_SUITS = {'Truempfe': ['S7', 'S8', 'S9', 'S10', 'SK', 'SA', 'HU',
                                    'HO', 'SU', 'SO', 'GU', 'GO', 'EU', 'EO'],
                       'Gras'    : ['G7', 'G8', 'G9', 'G10', 'GK', 'GA'],
                       'Eichel'  : ['E7', 'E8', 'E9', 'E10', 'EK', 'EA'],
                       'Herz'    : ['H7', 'H8', 'H9', 'H10', 'HK', 'HA']}

EICHEL_SOLO_SUITS = {'Schellen': ['S7', 'S8', 'S9', 'S10', 'SK', 'SA'],
                     'Gras'    : ['G7', 'G8', 'G9', 'G10', 'GK', 'GA'],
                     'Truempfe': ['E7', 'E8', 'E9', 'E10', 'EK', 'EA', 'HU',
                                  'HO', 'SU', 'SO',  'GU', 'GO', 'EU', 'EO'],
                     'Herz'    : ['H7', 'H8', 'H9', 'H10', 'HK', 'HA']}

STANDARD_MAPPING = reorder_dict(STANDARD_SUITS)


        
SUITS_MAPPING = {'Wenz'            : reorder_dict(WENZ_SUITS),
                 'Herz Solo'       : STANDARD_MAPPING,
                 'Gras Solo'       : reorder_dict(GRAS_SOLO_SUITS),
                 'Eichel Solo'     : reorder_dict(EICHEL_SOLO_SUITS),
                 'Schellen Solo'   : reorder_dict(SCHELLEN_SOLO_SUITS),
                 'Normale Schellen': STANDARD_MAPPING,
                 'Normale Gras'    : STANDARD_MAPPING,
                 'Normale Eichel'  : STANDARD_MAPPING,
                 'Ramsch'          : STANDARD_MAPPING,
                 None              : STANDARD_MAPPING}
 
# ========================== Miscellaneous ================================== #
       
GAME_MODE_TO_ACES = {'Normale Schellen': 'SA', 'Normale Eichel': 'EA',
                     'Normale Gras': 'GA'}


#SUIT_TO_CODE={'Schellen':'S','Gras':'G','Eichel':'E','Herz':'H'}

GAME_PRIORITY = {'Herz Solo': 1, 'Gras Solo': 1, 'Eichel Solo': 1,
                 'Schellen Solo': 1, 'Wenz': 2, 'Normale Schellen': 3,
                 'Normale Eichel': 3, 'Normale Gras': 3}

NORMAL_ORDERING = ['7', '8', '9', 'K', '10', 'A']
WENZ_ORDERING = ['7', '8', '9', 'O', 'K', '10', 'A']

# ============== Trump Ordering for all game modes ========================== #
NORMAL_TRUMP_ORDERING   = ['H7', 'H8', 'H9', 'HK', 'H10', 'HA', 'SU', 'HU' ,
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO']
WENZ_TRUMP_ORDERING     = ['SU', 'HU', 'GU', 'EU']
GRAS_TRUMP_ORDERING     = ['G7', 'G8', 'G9', 'GK', 'G10', 'GA', 'SU', 'HU',
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO']
EICHEL_TRUMP_ORDERING   = ['E7', 'E8', 'E9', 'EK', 'E10', 'EA', 'SU', 'HU',
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO']
SCHELLEN_TRUMP_ORDERING = ['S7', 'S8', 'S9', 'SK', 'S10', 'SA', 'SU', 'HU',
                           'GU', 'EU', 'SO', 'HO', 'GO', 'EO']

TRUMP_ORDERINGS = {'Wenz'            : WENZ_TRUMP_ORDERING,
                   'Herz Solo'       : NORMAL_TRUMP_ORDERING,
                   'Gras Solo'       : GRAS_TRUMP_ORDERING,
                   'Eichel Solo'     : EICHEL_TRUMP_ORDERING,
                   'Schellen Solo'   : SCHELLEN_TRUMP_ORDERING,
                   'Ramsch'          : NORMAL_TRUMP_ORDERING,
                   'Normale Schellen': NORMAL_TRUMP_ORDERING,
                   'Normale Gras'    : NORMAL_TRUMP_ORDERING,
                   'Normale Eichel'  : NORMAL_TRUMP_ORDERING}

# ============================ Points ======================================= #


#TRUMPS_NORMAL=['H7','H8','H9','H10','HK','HA','HU','HO',
#           'SU','SO','GU','GO','EU','EO'] ##### Do i even use this????????????



POINTS = {0 : ['S7', 'S8', 'S9', 'G7', 'G8', 'G9', 'H7' ,'H8' ,'H9' ,
               'E7', 'E8', 'E9'],
          11: ['SA', 'GA', 'HA', 'EA'],
          10: ['S10', 'G10', 'H10', 'E10'],
          4 : ['SK', 'GK', 'HK', 'EK'],
          3 : ['SO', 'GO', 'HO', 'EO'],
          2 : ['SU', 'GU', 'HU', 'EU']}

POINTS_REORDERED = reorder_dict(POINTS) ### misleading name.

