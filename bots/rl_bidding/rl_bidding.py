import numpy as np
from constants import constants as con

n_game_modes = len(con.GAME_MODES)

n_extra = 5
N_features = 32 + n_extra

weights = np.zeros(n_game_modes, N_features)

def guaranteed_losses(hand, ace):
    """ Identifies the lengths of a run of consecutive low-cards,
    i.e. 7, 8, 9... etc. It is very hard to win hands with these."""
    suit = ace[0]
    ordering = reversed(con.NORMAL_ORDERING)
    stop = False
    index = -1
    n = 0
    while not stop:
        card = suit + ordering[index]
        if card in hand:
            n += 1
            index -= 1
            if index == -8:
                stop = True
        else:
            stop = True
    return n

def make_features(hand):
    feature_vec = np.zeros(32 + n_extra)
    feature_vec[32] = 1 # bias

    b = HeuristicBot()
    feature_vec[33] = b.guaranteed_wins("Herz Solo", hand)
    feature_vec[34] = b.guaranteed_wins("Wenz", hand)
    for i, ace in enumerate(["EA_", "GA_", "HA_", "SA_"]):
        feature_vec[35 + 2*i] = b.find_runs(hand, ace)
        feature_vec[35 + 2*i + 1] = guaranteed_losses(hand, ace)

    return feature_vec


def sigmoid(features):
    dotprod = np.dot(weights, features)
    result = 1.0 / (1 + np.exp(-dotprod)) # has dimension n_game_modes
    return result

def sigmoid_derivative(features):
    sig = sigmoid(features)
    return np.outer(sig*(1 - sig), features) # wrong dimensions!

def policy(hand):
    options = sigmoid(make_features(hand))
    best_index = np.argmax(options)
    game_mode = reverse_action_map[best_index]
    return game_mode


alpha = 0.01

def update_weights(weights, action, result):
    index = action_map[action]
    derivative = sigmoid_derivative(weights, features)
    expected = sigmoid(weights, features)
    increment = [result - expected] * derivative

    new_weights = weights
    new_weights[:, index] += alpha * increment

    return new_weights









