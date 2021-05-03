import pacman
from pacman.problems import PositionSearchProblem
from pacman.agents import ClosestDotSearchAgent
from pacman import util
from ex03 import astar_search


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem (all its methods are
    inherited), but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    Look at ClosestDotSearchAgent in agents.py to understand how to implement the goal test.
    """

    def __init__(self, gameState, costFn=lambda x: 1):
        """Stores information from the gameState.  You don't need to change this."""
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = costFn
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will complete the problem definition.

        Hint: A goal state is any state resulting in some food being eaten.
        """
        x, y = state
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


if __name__ == '__main__':
    pacman.run(astar_search, problem=AnyFoodSearchProblem, agent=ClosestDotSearchAgent)