from pacman.game import Agent
from pacman.problems import PositionSearchProblem
from pacman import util
from ex01 import breadth_first_search


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem (all its methods are
    inherited), but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    Look at ClosestDotSearchAgent (given below) to understand how to implement the goal test.
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
        Fill this in with a goal test that will complete the problem definition.

        Hints:
         - The state is Pacman's position (x,y).
         - food.asList() returns the list of food positions.
         - A goal state is any position where Pacman eats some food.
        """
        x, y = state
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ClosestDotSearchAgent(Agent):
    """
    Eat all the food using a sequence of searches to the closest food

    THERE IS NOTHING TO CHANGE HERE.
    """

    def __init__(self, **kwargs):
        self.index = 0

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while currentState.getFood().count() > 0:
            problem = AnyFoodSearchProblem(currentState)  # Makes a new search problem
            segment = breadth_first_search(problem)  # Find a path
            self.actions += segment
            for action in segment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def getAction(self, state):
        i = self.actionIndex
        self.actionIndex += 1
        return self.actions[i] if i < len(self.actions) else 'Stop'


if __name__ == '__main__':
    import os
    os.system('python -m pacman -a ClosestDotSearchAgent -l mediumSearch')
