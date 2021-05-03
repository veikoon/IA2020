# heuristics.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
This file contains all of the heuristics that can be used in a search algorithm.
"""


def null_cost(position):
    """The cost for stepping into any position is always 0."""
    return 0


def all_equal_cost(position):
    """The cost for stepping into any position is always 1."""
    return 1


def stay_west_cost(position):
    """
    A cost function that penalizes being in positions on the East side of the board.
    The cost for stepping into a position (x,y) is 2^x.
    """
    return 2 ** position[0]


def stay_east_cost(position):
    """
    A cost function that penalizes being in positions on the West side of the board.
    The cost for stepping into a position (x,y) is 1/2^x.
    """
    return 0.5 ** position[0]


def null_heuristic(state, problem):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattan_heuristic(position, problem, info={}):
    """The Manhattan distance heuristic for a PositionSearchProblem"""
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclidean_heuristic(position, problem, info={}):
    """The Euclidean distance heuristic for a PositionSearchProblem"""
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5


def empty_search(problem):
    """A convenience function that returns an empty list"""
    return []