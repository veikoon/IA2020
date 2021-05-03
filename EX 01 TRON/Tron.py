import random
import time
import copy
import numpy
import numba
from numba import jit
## fenetre d'affichage

import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
plt.ion()
plt.show()
fig,axes = plt.subplots(1,1)
fig.canvas.set_window_title('TRON')


#################################################################################
#
#  Parametres du jeu

LARGEUR = 13
HAUTEUR = 17
L = 20  # largeur d'une case du jeu en pixel

canvas = None   # zone de dessin
Grille = None   # grille du jeu
posJ1  = None   # position du joueur 1 (x,y)
NbPartie = 0   # Nombre de parties effectuées
Scores = [0 , 0]  # score de la partie / total des scores des differentes parties

def InitPartie():  
    global Grille, PosJ1, NbPartie, Scores
    
    NbPartie += 1
    Scores[0] = 0
    
    Grille = numpy.zeros((LARGEUR,HAUTEUR))
    
    # #positionne les murs de l'arene
    for x in range(LARGEUR):
       Grille[x][0] = 10
       Grille[x][HAUTEUR-1] = 10
       
    for y in range(HAUTEUR):
       Grille[LARGEUR-1][y] = 10
       Grille[0][y] = 10
    
    Grille[6][6] = 10
    Grille[6][7] = 10
    Grille[6][8] = 10
    Grille[6][9] = 10
    Grille[6][10] = 10
    Grille[6][11] = 10
    Grille[6][12] = 10
    Grille[4][9] = 10
    Grille[5][9] = 10
    Grille[7][9] = 10
    Grille[8][9] = 10
    # position du joueur 1
    PosJ1 = (LARGEUR//2,1)


#################################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

def Play():   
    global Scores
    
    while (True):
      Tstart = time.time()
      global  PosJ1
      allowDir = getPos(Grille, PosJ1[0],PosJ1[1]) # recupere les deplacements possibles
      Grille[PosJ1[0]][PosJ1[1]] = 1 # laisse la trace de la moto
      #showGrille()

      if(len(allowDir) == 0): return
      
      #rand = random.randrange(len(allowPos))
      scores = []
      for d in allowDir:
        scores.append(MonteCarlo(Grille,PosJ1[0]+d[0],PosJ1[1]+d[1], 10000))
        
      m = max(scores)
      ind = scores.index(m)

      PosJ1 = ( PosJ1[0] + allowDir[ind][0]  , PosJ1[1] + allowDir[ind][1])  #deplacement


      # fin de traitement
      
      Scores[0] +=1 
      print(time.time()-Tstart)
      Affiche()
      
      # detection de la collision  
      
      if ( Grille[PosJ1[0]][PosJ1[1]] != 0 ): return
       
   
    
    
################################################################################
#    
# Dessine la grille de jeu


def Affiche():
    axes.clear()
    
    plt.xlim(0,20)
    plt.ylim(0,20)
    plt.axis('off')
    fig.patch.set_facecolor((0,0,0))
    
    axes.set_aspect(1)
    
    # dessin des murs

    Murs  = []
    Bords = []
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if ( Grille[x][y] == 10 ) : Bords.append(  plt.Rectangle((x,y), width = 1, height = 1 ) )
           if ( Grille[x][y] == 1  ) : Murs.append(  plt.Rectangle((x,y), width = 1, height = 1 ) )
        
    axes.add_collection (  matplotlib.collections.PatchCollection(Murs,   facecolors = (1.0, 0.47, 0.42)) )
    axes.add_collection (  matplotlib.collections.PatchCollection(Bords,  facecolors = (0.6, 0.6, 0.6)) )
    
    # dessin de la moto
  
    axes.add_patch(plt.Circle((PosJ1[0]+0.5,PosJ1[1]+0.5), radius= 0.5, facecolor = (1.0, 0, 0) ))
    
    # demande reaffichage
    fig.canvas.draw()
    fig.canvas.flush_events()  
 

################################################################################
#    
# Lancement des parties      
          
def GestionnaireDeParties():
    global Scores
   
    for i in range(3):
        time.sleep(1) # pause dune seconde entre chaque partie
        InitPartie()
        Play()
        Scores[1] += Scores[0]   # total des scores des parties
        Affiche()
        ScoMoyen = Scores[1]//(i+1)
        print("Partie " + str(i+1) + " === Score : " + str(Scores[0]) + " === Moy " + str(ScoMoyen) )

@jit   
def getPos(Grid,x,y):
  PosJ=[x,y]
  allowPos= []
  #print(PosJ1[0],PosJ1[1])
  if((PosJ[0]+1) <= LARGEUR-1 and (Grid[PosJ[0]+1][PosJ[1]])==0): allowPos.append((1,0))
  if((PosJ[0]-1) > 0 and (Grid[PosJ[0]-1][PosJ[1]])==0): allowPos.append((-1,0))
  if((PosJ[1]+1) <= HAUTEUR-1 and (Grid[PosJ[0]][PosJ[1]+1])==0): allowPos.append((0,1))
  if((PosJ[1]-1) > 0 and (Grid[PosJ[0]][PosJ[1]-1])==0): allowPos.append((0,-1))
  return allowPos
     
def showGrille():
  for i in range(len(Grille)):
    print(Grille[i])

@jit
def SimulationPartie(Tab,x,y):
  scoring = 0
  while True:
    L = getPos(Tab,x,y)
    if(len(L) == 0):return scoring
    rand = random.randrange(len(L))
    Tab[x][y] = 1 # laisse la trace de la moto
    scoring += 1
    x = x + L[rand][0]
    y = y + L[rand][1]
    
@jit
def MonteCarlo(Grid,x,y,nombreParties):
  Total = 0
  compt = 0
  for i in range(nombreParties):
    Grid2 = numpy.copy(Grid)
    Total += SimulationPartie(Grid2,x,y)
  return Total

GestionnaireDeParties()
