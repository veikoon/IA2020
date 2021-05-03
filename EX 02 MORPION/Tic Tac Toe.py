import tkinter
from tkinter import messagebox
import random
import os
import copy

#################################################################################
#
#  Parametres du jeu

canvas = None   # zone de dessin

#Grille[0][0] désigne la case en haut à gauche
#Grille[2][0] désigne la case en haut à droite
#Grille[0][2] désigne la case en bas à gauche


Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Scores = [0,0]   # score du joueur 1 (Humain) et 2 (IA)



#



###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

def Play(x,y):             
    if(Grille[x][y] == 0): Grille[x][y] = 1
    else: return
    done = False
    if(not getEmptyCells(Grille)): return
    """while done:
        xp = random.randrange(3)
        yp = random.randrange(3)
        if(Grille[xp][yp] == 0):
            Grille[xp][yp] = 2
            done = False"""
    Pos = JoueursSimuleIA(Grille)[1]
    print("Pos", Pos)
    Grille[Pos[0]][Pos[1]] = 2

def getEmptyCells(Grid):
    emptyCase = []
    for i in range(3):
        for j in range(3):
            if(Grid[i][j] == 0): 
                emptyCase.append((i,j))
    return emptyCase

def isReset():
    if(getEmptyCells(Grille)): Reset()

def Reset():
    global Grille
    Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]

def ShowGrid(Grid):
    for i in range(3):
        print(Grid[i])
    print()
   
def CheckWin(Grid):
    for i in range(3):
        #Lignes
        if((Grid[i][0] != 0) and (Grid[i][0] == Grid[i][1]) and (Grid[i][0] == Grid[i][2])):
            return Grid[i][0]-1
        #Colonnes
        if((Grid[0][i] != 0) and (Grid[0][i] == Grid[1][i]) and (Grid[0][i] == Grid[2][i])):
            return Grid[0][i]-1
    #Diagonales
    if(Grid[0][0] != 0 and (Grid[0][0] == Grid[1][1]) and (Grid[0][0] == Grid[2][2])):
        return Grid[0][0]-1
    if(Grid[2][0] != 0 and (Grid[2][0] == Grid[1][1]) and (Grid[2][0] == Grid[0][2])):
        return Grid[2][0]-1
    return 3

def isWin(player):
    if(CheckWin(Grille) != 3):
        Scores[player] += 1
        os.system("sleep 1")
        Reset()
    if(not getEmptyCells(Grille)):
        Reset()


def JoueurSimuleHumain(Grid):
    if(CheckWin(Grid)!=3 or not getEmptyCells(Grid)): 
        return (CalculScore(Grid))
    L = getEmptyCells(Grid)
    Resultats = []
    for coup in L:
        Grid2 = copy.deepcopy(Grid)
        Grid2[coup[0]][coup[1]] = 1

        Score = JoueursSimuleIA(Grid2)
        Resultats.append((Score[0], coup))

    return max(Resultats, key = lambda x: x[0])

def JoueursSimuleIA(Grid):
    if(CheckWin(Grid)!=3 or not getEmptyCells(Grid)): 
        return (CalculScore(Grid))
    L = getEmptyCells(Grid)
    Resultats = []
    for coup in L:
        Grid2 = copy.deepcopy(Grid)
        Grid2[coup[0]][coup[1]] = 2

        Score = JoueurSimuleHumain(Grid2)
        Resultats.append((Score[0], coup))
        
    return min(Resultats, key = lambda x: x[0])


def CalculScore(Grid):
    if(CheckWin(Grid) == 1): return (0,1)
    elif(CheckWin(Grid) == 0): return (1,0)
    else: return (0,0)
    
    
################################################################################
#    
# Dessine la grille de jeu

def Affiche(PartieGagnee = 3):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        if (PartieGagnee == 0) : fillcoul = 'red'
        elif (PartieGagnee == 1) : fillcoul = 'yellow'
        else : fillcoul = 'gray'
        
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill=fillcoul, width="4" )
            canvas.create_line(0,i*100,300,i*100,fill=fillcoul, width="4" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        
        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])

        canvas.create_text(150,400, font=('Helvetica', 30), text = msg, fill=fillcoul)  
        
    
        canvas.update()   #force la mise a jour de la zone de dessin
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
   
    window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    
    #print("clicked at", x,y)
    
    Play(x,y)  # gestion du joueur humain et de l'IA
    Affiche()
    #ShowGrid()

    isWin(CheckWin(Grille))

    if (Scores[0] == Scores[1]): val = 3
    else : val = Scores.index(max(Scores))
    Affiche(val)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

# fenetre
window = tkinter.Tk()
window.geometry("300x500") 
window.title('Mon Super Jeu')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", MouseClick)

#zone de dessin
WIDTH = 300
HEIGHT = 500
canvas = tkinter.Canvas(window, width=WIDTH , height=HEIGHT, bg="#000000")
canvas.place(x=0,y=0)
Affiche()
 
# active la fenetre 
window.mainloop()