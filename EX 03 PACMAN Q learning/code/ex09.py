from itertools import cycle
from pacman.util import Counter, raiseNotDefined

def mdp_parameters(type):
    """
    Return the parameters for the DiscountGrid MDP leading to different types of policy:
     a) Prefer the close exit (+1), risking the cliff (-10).
     b) Prefer the close exit (+1), but avoiding the cliff (-10).
     c)	Prefer the distant exit (+10), risking the cliff (-10).
     d)	Prefer the distant exit (+10), avoiding the cliff (-10).
    """
    if type == 'a':
        discount = None
        noise = None
        reward = None

    elif type == 'b':
        discount = None
        noise = None
        reward = None

    elif type == 'c':
        discount = None
        noise = None
        reward = None

    elif type == 'd':
        discount = None
        noise = None
        reward = None

    return discount, noise, reward

