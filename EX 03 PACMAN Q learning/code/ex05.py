
def corners_heuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid (game.py)

    "*** YOUR CODE HERE ***"
    return 0


if __name__ == '__main__':
    import os
    os.system('python -m pacman -a SearchAgent -p CornersSearchProblem -s astar_search -f corners_heuristic -l mediumCorners')
