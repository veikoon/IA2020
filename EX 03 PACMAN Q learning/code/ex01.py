from pacman.util import Queue


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.

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


def path_reconstruction(start, goal, explored):
    # *** YOUR CODE HERE *** #
    return []


if __name__ == '__main__':
    import os
    os.system('python -m pacman -a SearchAgent -s breadth_first_search -l tinyMaze')
    os.system('python -m pacman -a SearchAgent -s breadth_first_search -l mediumMaze')
    os.system('python -m pacman -a SearchAgent -s breadth_first_search -l bigMaze -z 0.5')
