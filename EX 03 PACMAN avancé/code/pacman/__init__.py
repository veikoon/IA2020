import sys
from optparse import OptionParser
from .layout import getLayout
from .environment import runGames
from .agents import SearchAgent
from .problems import PositionSearchProblem, FoodSearchProblem
from .heuristics import *
from .graphicsDisplay import PacmanGraphics
from .util import lookup


def run(search_algorithm, problem=None, heuristic=None, agent=None):

    # options
    parser = OptionParser()
    parser.add_option('-l', dest='layout', type='string', default='tinyMaze', help='Layout file from which to load the map')
    parser.add_option('-c', dest='cost', type='string', default='all_equal', help='Function for computing the mouvement costs')
    parser.add_option('-f', dest='heuristic', type='string', default='null', help='Function name of the heuristic')
    parser.add_option('-p', dest='problem', type='string', default='Position', help='Class name of the search problem')
    parser.add_option('-z', dest='zoom', type='float',  default=1.0, help='Zoom the size of the graphics window')
    parser.add_option('-t', dest='time', type='float',  default=0.1, help='Time to delay between frames; <0 means keyboard')
    args, _ = parser.parse_args(sys.argv)

    # setup
    cost_fn = globals()[args.cost+'_cost']
    heurist = globals()[args.heuristic+'Heuristic'] if heuristic is None else heuristic
    problem = globals()[args.problem+'SearchProblem'] if problem is None else problem
    display = PacmanGraphics(args.zoom, args.time)
    layout = getLayout(args.layout)
    agent = SearchAgent if agent is None else agent
    pacman = agent(search_algorithm, problem, costFn=cost_fn, heuristic=heurist, display=display)
    ghosts = []

    # launch
    runGames(layout, pacman, ghosts, display)
