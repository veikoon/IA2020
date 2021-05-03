import pacman
from pacman.util import PriorityQueue
from ex01 import path_reconstruction


def astar_search(problem, heuristic):
    """
    Search the node that has the lowest total cost (past + future) first.

    The heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. It takes two inputs: a state and a problem.

    >>> heuristic(state, problem)
    11.2

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
    pacman.run(astar_search)
