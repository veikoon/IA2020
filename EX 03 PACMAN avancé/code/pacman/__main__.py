from pacman.layout import getLayout
from pacman.environment import runGames
from pacman.keyboard import KeyboardAgent
from pacman.ghosts import RandomGhost
import random

random.seed('cs188')

layout = getLayout('mediumClassic')
pacman = KeyboardAgent()
ghosts = [RandomGhost(i+1) for i in range(2)]

runGames(layout, pacman, ghosts)
