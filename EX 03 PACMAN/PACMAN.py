import pygame
import random
import copy
 
#################################################################
##
##  variables du jeu 
 
# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]

# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]
CYAN  = [ 0, 255 ,255]
ORANGE = [255, 165, 0 ]
PINK = [ 255,105,180]
YELLOW = [255,255,0]          

   
ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels
HAUTEUR = len(TBL)     # nb de cases en hauteur
LARGEUR = len(TBL[0])  # nb de cases en largeur


def PlacementsGUM():  # placements des pacgums
   GUM = []
   for t in range(HAUTEUR):
      GUM.append([0]*LARGEUR)
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[y][x] == 0):
            GUM[y][x] = 1
   return GUM

def CreateDistanceTab():
	DistTab = copy.deepcopy(GUM)
	for i in range(len(GUM)):
		for j in range(len(GUM[0])):
			if(GUM[i][j] == 1):
				DistTab[i][j] = 0
			else:
				DistTab[i][j] = 100
			if(TBL[i][j] == 1):
				DistTab[i][j] = 9999

	return DistTab
            
def CreateDistanceTabPac():
	global PacManPos
	DistTab = copy.deepcopy(GUM)
	for i in range(len(GUM)):
		for j in range(len(GUM[0])):
			if(TBL[i][j] == 0):
				DistTab[i][j] = 100
			if(TBL[i][j] == 1 or TBL[i][j] == 2):
				DistTab[i][j] = 9999
	DistTab[PacManPos[1]][PacManPos[0]] = 0
	return DistTab

GUM = PlacementsGUM()
TBLDist = CreateDistanceTab()
SCORE = 0
PacManPos = [5,5]
TBLDistPac = CreateDistanceTabPac()
Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  PINK, (0,-1)]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  ORANGE, (0,-1)] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  CYAN, (0,-1)]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  RED, (0,-1)]    )

#################################################################
##
##  INIT FENETRE 


# Setup
pygame.init()
police = pygame.font.SysFont("arial", 22)
screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
screen = pygame.display.set_mode((screeenWidth,screenHeight))
pygame.display.set_caption("ESIEE - PACMAN")
done = False
clock = pygame.time.Clock()   
pygame.mouse.set_visible(True) 
 
 
#################################################################
##
##  FNT AFFICHAGE



def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine les murs et les stockes dans un buffer
def CreateDecor():
   fond = pygame.Surface((screeenWidth,screenHeight))
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[y][x] == 1 and TBL[y][x+1] == 1 ):
            xx = To(x)
            yy = To(y)
            e = EPAISS // 2
            pygame.draw.rect(fond,BLUE,[xx,yy-e, ZOOM,EPAISS],0)

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[y][x] == 1 and TBL[y+1][x] == 1 ):
            xx = To(x) 
            yy = To(y)
            e = EPAISS // 2
            pygame.draw.rect(fond,BLUE,[xx-e,yy, EPAISS,ZOOM],0)
            
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[y][x] == 1):
            xx = To(x) 
            yy = To(y)
            e = EPAISS // 2
            pygame.draw.ellipse(fond,BLUE,[xx-e,yy-e, EPAISS,EPAISS],0)
   return fond
   
 
            
DECOR = CreateDecor()
 
# dessine l'ensemble des éléments du jeu par dessus le décor
anim_bouche = 0
def Dessine():
   global anim_bouche
   screen.fill(BLACK)
   screen.blit(DECOR,(0,0))
   
   #dessine les bonbons
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[y][x] == 1):
            xx = To(x) 
            yy = To(y)
            e = 4
            pygame.draw.ellipse(screen,WHITE,[xx-e,yy-e, 2*e, 2*e],0)
   
   #dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   pygame.draw.ellipse(screen,YELLOW,[xx-e,yy-e, 2*e, 2*e],0)
    
   
   anim = [ 5, 10, 15,  10]
   anim_bouche = (anim_bouche+1)%len(anim)
   ouv_bouche = anim[anim_bouche] 
   bouche = [(xx,yy),(xx+e,yy-ouv_bouche),(xx+e,yy+ouv_bouche)]
   
   
   
   pygame.draw.polygon(screen, BLACK, bouche)
   
   
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 15
      
      pygame.draw.ellipse(screen,P[2],[dec+xx-e,yy-e, 2*e, 2*e],0)
      pygame.draw.rect(screen,P[2],[dec+xx-e,yy, 2*e, e],0)
      t = 10
      pygame.draw.ellipse(screen,WHITE,[dec+xx-7-t//2,yy-t//2, t, t],0)
      pygame.draw.ellipse(screen,WHITE,[dec+xx+7-t//2,yy-t//2, t, t],0)
      t = 6
      pygame.draw.ellipse(screen,BLACK,[dec+xx-7-t//2,yy-t//2, t, t],0)
      pygame.draw.ellipse(screen,BLACK,[dec+xx+7-t//2,yy-t//2, t, t],0)
      
      dec += 3
     
   # affiche texte
   zone = police.render( str(SCORE), True, YELLOW)
   screen.blit(zone,(300,screenHeight - 50))
            
#################################################################
##
##  IA RANDOM


      
def PacManPossibleMove():
   L = []
   x = PacManPos[0]
   y = PacManPos[1]
   if ( TBL[y-1][x  ] == 0 ): L.append((0,-1))
   if ( TBL[y+1][x  ] == 0 ): L.append((0, 1))
   if ( TBL[y  ][x+1] == 0 ): L.append(( 1,0))
   if ( TBL[y  ][x-1] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[y-1][x  ] != 1 ): L.append((0,-1))
   if ( TBL[y+1][x  ] != 1 ): L.append((0, 1))
   if ( TBL[y  ][x+1] != 1 ): L.append(( 1,0))
   if ( TBL[y  ][x-1] != 1 ): L.append((-1,0))
   return L

def show(grid):
	for i in range(len(grid)):
		print(grid[i])
	print("#####")
   
def IA():
	global PacManPos, Ghosts, SCORE, TBLDist
	#deplacement Pacman

	for p in Ghosts:
		if(TBLDistPac[p[1]][p[0]] <= 3):
			if(PacManPos[0]>p[0] and TBLDist[PacManPos[1]][PacManPos[0] - 1] != 9999):
				TBLDist[PacManPos[1]][PacManPos[0] - 1] = 100
			if(PacManPos[0]<p[0]  and TBLDist[PacManPos[1]][PacManPos[0] + 1] != 9999):
				TBLDist[PacManPos[1]][PacManPos[0] + 1] = 100
			if(PacManPos[1]>p[1]  and TBLDist[PacManPos[1] - 1][PacManPos[0]] != 9999):
				TBLDist[PacManPos[1] - 1][PacManPos[0]] = 100
			if(PacManPos[1]<p[1]  and TBLDist[PacManPos[1] + 1][PacManPos[0]] != 9999):
				TBLDist[PacManPos[1] + 1][PacManPos[0]] = 100

	L = PacManPossibleMove()

	val = []
	for k in L:
		val.append(TBLDist[PacManPos[1]+k[1]][PacManPos[0]+k[0]])

	choix = val.index(min(val))
	PacManPos[0] += L[choix][0]	
	PacManPos[1] += L[choix][1]

	CheckCollision()

	if(GUM[PacManPos[1]][PacManPos[0]] == 1):
		GUM[PacManPos[1]][PacManPos[0]] = 0
	SCORE += 100

	#deplacement Fantome
	for F in Ghosts:
		L = GhostsPossibleMove(F[0],F[1])
		if(F[3] in L):
			choix = L.index(F[3])
		else:
			if(F[3] == (0,1)): L.remove((0,-1))
			if(F[3] == (1,0)): L.remove((-1,0))
			if(F[3] == (0,-1)): L.remove((0,1))
			if(F[3] == (-1,0)): L.remove((1,0))
			choix = random.randrange(len(L))
			F[3] = L[choix]

		F[0] += L[choix][0]
		F[1] += L[choix][1]

def UpdateDist():
	global TBLDist
	TBLDist = CreateDistanceTab()
	done = True
	while done:
		done = False
		for i in range(len(TBLDist)):
			for j in range(len(TBLDist[0])):
				if(TBLDist[i][j] != 9999):
					if(TBLDist[i][j] >= 0):
						val = []
						val.append(TBLDist[i+1][j])
						val.append(TBLDist[i-1][j])
						val.append(TBLDist[i][j+1])
						val.append(TBLDist[i][j-1])
						tempmin = min(val) + 1
						if(TBLDist[i][j] > tempmin):
							TBLDist[i][j] = tempmin
							done = True

def UpdateDistPac():
	global TBLDistPac
	TBLDistPac = CreateDistanceTabPac()
	done = True
	while done:
		done = False
		for i in range(len(TBLDistPac)):
			for j in range(len(TBLDistPac[0])):
				if(TBLDistPac[i][j] != 9999):
					if(TBLDistPac[i][j] >= 0):
						val = []
						val.append(TBLDistPac[i+1][j])
						val.append(TBLDistPac[i-1][j])
						val.append(TBLDistPac[i][j+1])
						val.append(TBLDistPac[i][j-1])
						tempmin = min(val) + 1
						if(TBLDistPac[i][j] > tempmin):
							TBLDistPac[i][j] = tempmin
							done = True

def CheckCollision():
	global done
	for g in Ghosts:
		if(PacManPos[0] == g[0] and PacManPos[1] == g[1]):
			done = True
			print("collision")

def CheckRemainingGum():
	global done
	verif = True
	for i in range(len(GUM)):
		for j in range(len(GUM[0])):
			if(GUM[i][j]==1 and done == False):
				verif = False
	done = verif
 

#################################################################
##
##   GAME LOOP


# -------- Main Program Loop -----------
while not done:
   event = pygame.event.Event(pygame.USEREVENT)    
   pygame.event.pump()
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
   IA()

   UpdateDist()
   UpdateDistPac()

   Dessine()
   
   CheckRemainingGum()

   pygame.display.flip()
 
    # Limit frames per second
   clock.tick(4)
 
# Close the window and quit.
pygame.quit()