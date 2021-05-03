import random
import pickle
from optparse import OptionParser

from .layout import getLayout
from .api import runGames, replayGame
from . import textDisplay, graphicsDisplay

from .keyboard import KeyboardAgent
from .ghosts import RandomGhost, DirectionalGhost
from .agents import SearchAgent, LeftTurnAgent, GreedyAgent
from .problems import PositionSearchProblem, FoodSearchProblem
from .heuristics import *
from .extractors import IdentityExtractor, SimpleExtractor, CoordinateExtractor


def parseOptions():
    """
    Processes the command used to run pacman from the command line.
    """

    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = OptionParser(usageStr)

    parser.add_option('-l', dest='layout', help='the layout file to use [Default: %default]', default='mediumClassic')
    parser.add_option('-a', dest='agent', help='the pacman agent to use [Default: %default]', default='KeyboardAgent')
    parser.add_option('-p', dest='problem', type='string', default='PositionSearchProblem', help='the search problem to use [Default: %default]')
    parser.add_option('-s', dest='search', type='string', default='empty_search', help='the search algorithm to use [Default: %default]')
    parser.add_option('-c', dest='cost', type='string', default='all_equal', help='the cost function to use [Default: %default]')
    parser.add_option('-f', dest='heuristic', type='string', default='null_heuristic', help='the heuristic to use [Default: %default]')
    parser.add_option('-e', dest='extractor', type='string', default='Identity', help='the feature extractor to use [Default: %default]')
    parser.add_option('-n', dest='numGames', type='int', help='the number of GAMES to play [Default: %default]', metavar='GAMES', default=1)
    parser.add_option('-x', dest='numTraining', type='int', help='How many episodes are training [Default: %default]', default=0)
    parser.add_option('-g', dest='ghost', help='the ghost agent to use [Default: %default]', default='RandomGhost')
    parser.add_option('-k', dest='numGhosts', type='int', help='The maximum number of ghosts to use [Default: %default]', default=4)
    parser.add_option('-z', dest='zoom', type='float', help='Zoom the size of the graphics window [Default: %default]', default=1.0)
    parser.add_option('-r', dest='gameToReplay', help='A recorded game file (pickle) to replay', default=None)
    parser.add_option('-d', dest='delay', type='float', help='Time to delay between frames [Default: %default]', default=0.1)
    parser.add_option('-t', dest='timeout', type='int', help='Maximum time spent on a single game [Default: %default]', default=30)
    parser.add_option('--seed', action='store_true', dest='fixRandomSeed', help='Fixes the random seed to always play the same game', default=False)
    parser.add_option('--record', action='store_true', dest='record', help='Writes game to a file (named by the time it was played)', default=False)
    parser.add_option('--text', action='store_true', dest='textGraphics', help='Display output as text only', default=False)
    parser.add_option('--quiet', action='store_true', dest='quietGraphics', help='Generate minimal output and no graphics', default=False)
    parser.add_option('--catch', action='store_true', dest='catch',  help='Turns on exception handling and timeouts during games', default=False)

    args, otherjunk = parser.parse_args()

    # check integrity
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    # check conflicts
    noKeyboard = args.gameToReplay is None and (args.textGraphics or args.quietGraphics)
    if noKeyboard and args.pacman.startswith('Keyboard'):
        raise Exception('Using the keyboard requires graphics (not text display)')

    return args


def run(namespace={}):

    # Process the command line
    options = parseOptions()

    # Fix the random seed
    if options.fixRandomSeed:
        random.seed('cs188')

    # Choose a display format
    if options.quietGraphics:
        display = textDisplay.NullGraphics()
    elif options.textGraphics:
        textDisplay.SLEEP_TIME = options.frameTime
        display = textDisplay.PacmanGraphics()
    else:
        display = graphicsDisplay.PacmanGraphics(options.zoom, options.delay)

    # Choose a layout
    layout = getLayout(options.layout)
    if layout is None:
        raise Exception("The layout " + options.layout + " cannot be found")
    print('\n')
    print('=====', options.layout, '=====')

    # Choose a ghost agent
    ghostType = globals()[options.ghost]
    ghosts = [ghostType(i + 1) for i in range(options.numGhosts)]

    # Choose a Pacman agent
    namespace.update(**globals())
    agentOpts = dict(
        display=display,
        search=namespace[options.search],
        problem=namespace[options.problem],
        costFn=namespace[options.cost + '_cost'],
        heuristic=namespace[options.heuristic],
        extractor=namespace[options.extractor + 'Extractor'],
        numTraining=options.numTraining,
    )
    agentType = namespace[options.agent]
    pacman = agentType(**agentOpts)

    # Special case: recorded games don't use the runGames method or args structure
    if options.gameToReplay is not None:
        print('Replaying recorded game %s.' % options.gameToReplay)
        with open(options.gameToReplay, 'rb') as f:
            recorded = pickle.load(f)
        recorded['display'] = display
        replayGame(**recorded)
        return

    # Run pacman
    runGames(layout, pacman, ghosts, display, options.zoom, options.numGames, options.record, options.numTraining, options.catch, options.timeout)
