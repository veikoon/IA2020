from pacman.util import PriorityQueue
from ex01 import path_reconstruction


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.

    These are the functions to interact with the Pacman world:

    >>> state = problem.getStartState()
    >>> state
    (5, 5)

    >>> problem.getSuccessors(state)
    [((5, 4), 'South', 1), ((4, 5), 'West', 1)]

    >>> problem.isGoalState(state)
    False
    """

    # *** YOUR CODE HERE *** #
    return []


if __name__ == '__main__':
    import os
    os.system('python -m pacman -a SearchAgent -s uniform_cost_search -l mediumMaze')
    os.system('python -m pacman -a SearchAgent -s uniform_cost_search -l mediumMaze -c stay_east')
    os.system('python -m pacman -a SearchAgent -s uniform_cost_search -l mediumMaze -c stay_west')
