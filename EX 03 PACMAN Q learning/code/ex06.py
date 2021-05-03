from pacman.problems import PositionSearchProblem
from ex03 import astar_search


def manhattan_distance(start, goal):
    """Distance from start to goal ignoring walls"""
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def lazy_maze_distance(start, goal, problem):
    """Shortest path distance from start to goal"""
    if (start, goal) not in problem.heuristicInfo:
        prob = PositionSearchProblem(problem.startingGameState, start=tuple(start), goal=tuple(goal), warn=False, visualize=False)
        path = astar_search(prob, lambda s, p: 0)
        dist = len(path)
        problem.heuristicInfo[(start, goal)] = dist
    return problem.heuristicInfo[(start, goal)]


def food_heuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem. For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    return 0


if __name__ == '__main__':
    import os
    os.system('python -m pacman -a SearchAgent -p FoodSearchProblem -s astar_search -f food_heuristic -l tinySearch')
    os.system('python -m pacman -a SearchAgent -p FoodSearchProblem -s astar_search -f food_heuristic -l trickySearch')
