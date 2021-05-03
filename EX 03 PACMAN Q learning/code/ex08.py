from collections import defaultdict
from pacman.util import raiseNotDefined


def value_iteration(mdp, discount, iterations):
    """
    Value iteration is an algorithm that estimates the Q-values of an MDP.
    It runs for the given number of iterations, using the supplied discount factor.

    Some useful MDP methods you will use:
        mdp.getStates()
        mdp.getPossibleActions(state)
        mdp.getTransitionStatesAndProbs(state, action)
        mdp.getReward(state, action, nextState)
        mdp.isTerminal(state)
    """
    q_table = defaultdict(lambda: defaultdict(float))  # dict of dicts with default 0
    v_table = defaultdict(float)

    for k in range(iterations):
        "*** YOUR CODE HERE ***"
        raiseNotDefined()

    return q_table
