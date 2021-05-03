import optparse, sys, random

from pacman.learning import ValueIterationAgent
from gridworld.api import GridworldEnvironment, getUserAction, runEpisode
from gridworld.api import getCliffGrid, getCliff2Grid, getDiscountGrid, getBridgeGrid, getBookGrid, getMazeGrid
from gridworld.textGridworldDisplay import TextGridworldDisplay
from gridworld.graphicsGridworldDisplay import GraphicsGridworldDisplay


def parseOptions():
    optParser = optparse.OptionParser()
    optParser.add_option('-a', '--agent', action='store', metavar="A",
                         type='string', dest='agent', default="keyboard",
                         help='Agent type (options are \'random\', \'value\' and \'q\', default %default)')
    optParser.add_option('-d', '--discount',action='store',
                         type='float',dest='discount',default=0.9,
                         help='Discount on future (default %default)')
    optParser.add_option('-r', '--reward',action='store',
                         type='float',dest='livingReward',default=0.0,
                         metavar="R", help='Reward for living for a time step (default %default)')
    optParser.add_option('-n', '--noise',action='store',
                         type='float',dest='noise',default=0.2,
                         metavar="P", help='How often action results in ' +
                         'unintended direction (default %default)' )
    optParser.add_option('-e', '--epsilon',action='store',
                         type='float',dest='epsilon',default=0.3,
                         metavar="E", help='Chance of taking a random action in q-learning (default %default)')
    optParser.add_option('-l', '--learningRate',action='store',
                         type='float',dest='learningRate',default=0.5,
                         metavar="P", help='TD learning rate (default %default)' )
    optParser.add_option('-i', '--iterations',action='store',
                         type='int',dest='iters',default=10,
                         metavar="K", help='Number of rounds of value iteration (default %default)')
    optParser.add_option('-k', '--episodes',action='store',
                         type='int',dest='episodes',default=1,
                         metavar="K", help='Number of epsiodes of the MDP to run (default %default)')
    optParser.add_option('-g', '--grid',action='store',
                         metavar="G", type='string',dest='grid',default="Book",
                         help='Grid to use (case sensitive; options are BookGrid, BridgeGrid, CliffGrid, MazeGrid, default %default)' )
    optParser.add_option('-w', '--windowSize', metavar="X", type='int',dest='gridSize',default=150,
                         help='Request a window width of X pixels *per grid cell* (default %default)')
    optParser.add_option('-t', '--text',action='store_true',
                         dest='textDisplay',default=False,
                         help='Use text-only ASCII display')
    optParser.add_option('-p', '--pause',action='store_true',
                         dest='pause',default=False,
                         help='Pause GUI after each time step when running the MDP')
    optParser.add_option('-q', '--quiet',action='store_true',
                         dest='quiet',default=False,
                         help='Skip display of any learning episodes')
    optParser.add_option('-s', '--speed',action='store', metavar="S", type=float,
                         dest='speed',default=0.25,
                         help='Speed of animation, S > 1.0 is faster, 0.0 < S < 1.0 is slower (default %default)')
    optParser.add_option('-m', '--manual',action='store_true',
                         dest='manual',default=False,
                         help='Manually control agent')
    optParser.add_option('-v', '--valueSteps',action='store_true' ,default=False,
                         help='Display each step of value iteration')

    opts, args = optParser.parse_args()

    if opts.agent == 'keyboard':
        opts.manual = True

    if opts.manual and opts.agent != 'q':
        print('## Disabling Agents in Manual Mode (-m) ##')
        opts.agent = None

    # MANAGE CONFLICTS
    if opts.textDisplay or opts.quiet:
        opts.pause = False

    if opts.manual:
        opts.pause = True

    return opts


def run(namespace={}):

    opts = parseOptions()

    ###########################
    # GET THE GRIDWORLD
    ###########################

    mdpFunction = globals()["get"+opts.grid+"Grid"]
    mdp = mdpFunction()
    mdp.setLivingReward(opts.livingReward)
    mdp.setNoise(opts.noise)
    env = GridworldEnvironment(mdp)


    ###########################
    # GET THE DISPLAY ADAPTER
    ###########################

    display = TextGridworldDisplay(mdp)
    if not opts.textDisplay:
        display = GraphicsGridworldDisplay(mdp, opts.gridSize, opts.speed)
    try:
        display.start()
    except KeyboardInterrupt:
        sys.exit(0)

    ###########################
    # GET THE AGENT
    ###########################

    namespace.update(**globals())

    a = None
    if opts.agent == 'value':
        a = ValueIterationAgent(namespace['value_iteration'], mdp, opts.discount, opts.iters)
    elif opts.agent == 'q':
        actionFn = lambda state: mdp.getPossibleActions(state)
        qLearnOpts = {'gamma': opts.discount, 'alpha': opts.learningRate, 'epsilon': opts.epsilon, 'actionFn': actionFn}
        a = namespace['QLearningAgent'](**qLearnOpts) # TODO: mettere i parametri esplicitamente (togliere dict)
    elif opts.agent == 'random':
        # No reason to use the random agent without episodes
        if opts.episodes == 0:
            opts.episodes = 10
        class RandomAgent:
            def getAction(self, state):
                return random.choice(mdp.getPossibleActions(state))
            def getValue(self, state):
                return 0.0
            def getQValue(self, state, action):
                return 0.0
            def getPolicy(self, state):
                "NOTE: 'random' is a special policy value; don't use it in your code."
                return 'random'
            def update(self, state, action, nextState, reward):
                pass
        a = RandomAgent()
    else:
        if not opts.manual:
            raise Exception('Unknown agent type: '+opts.agent)


    ###########################
    # RUN EPISODES
    ###########################
    # DISPLAY Q/V VALUES BEFORE SIMULATION OF EPISODES
    try:
        if not opts.manual and opts.agent == 'value':
            if opts.valueSteps:
                for i in range(opts.iters):
                    value_iteration = namespace['value_iteration']
                    tempAgent = ValueIterationAgent(value_iteration, mdp, opts.discount, i)
                    display.displayValues(tempAgent, message = "VALUES AFTER "+str(i)+" ITERATIONS")
                    display.pause()

            display.displayValues(a, message = "VALUES AFTER "+str(opts.iters)+" ITERATIONS")
            display.pause()
            display.displayQValues(a, message = "Q-VALUES AFTER "+str(opts.iters)+" ITERATIONS")
            display.pause()
    except KeyboardInterrupt:
        sys.exit(0)



    # FIGURE OUT WHAT TO DISPLAY EACH TIME STEP (IF ANYTHING)
    displayCallback = lambda x: None
    if not opts.quiet:
        if opts.manual and opts.agent == None:
            displayCallback = lambda state: display.displayNullValues(state)
        else:
            if opts.agent in ('random', 'value'):
                displayCallback = lambda state: display.displayValues(a, state, "CURRENT VALUES")
            if opts.agent == 'q': displayCallback = lambda state: display.displayQValues(a, state, "CURRENT Q-VALUES")

    messageCallback = lambda x: print(x)
    if opts.quiet:
        messageCallback = lambda x: None

    # FIGURE OUT WHETHER TO WAIT FOR A KEY PRESS AFTER EACH TIME STEP
    pauseCallback = lambda : None
    if opts.pause:
        pauseCallback = lambda : display.pause()

    # FIGURE OUT WHETHER THE USER WANTS MANUAL CONTROL (FOR DEBUGGING AND DEMOS)
    if opts.manual:
        decisionCallback = lambda state : getUserAction(state, mdp.getPossibleActions)
    else:
        decisionCallback = a.getAction

    # RUN EPISODES
    if opts.episodes > 0:
        print()
        print("RUNNING", opts.episodes, "EPISODES")
        print()
    returns = 0
    for episode in range(1, opts.episodes+1):
        returns += runEpisode(a, env, opts.discount, decisionCallback, displayCallback, messageCallback, pauseCallback, episode)
    if opts.episodes > 0:
        print()
        print("AVERAGE RETURNS FROM START STATE: "+str((returns+0.0) / opts.episodes))
        print()
        print()

    # DISPLAY POST-LEARNING VALUES / Q-VALUES
    if opts.agent == 'q' and not opts.manual:
        try:
            display.displayQValues(a, message = "Q-VALUES AFTER "+str(opts.episodes)+" EPISODES")
            display.pause()
            display.displayValues(a, message = "VALUES AFTER "+str(opts.episodes)+" EPISODES")
            display.pause()
        except KeyboardInterrupt:
            sys.exit(0)