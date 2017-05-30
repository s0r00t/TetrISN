from gs import GameState
from pygame import Surface, transform
from pygame.draw import rect
from pygame.event import Event, post
from pygame.font import Font
from pygame.locals import KEYDOWN
from pygame.time import set_timer
from random import randint
from utils import *
import pickle
import sys

class IGState(GameState):
    def __init__(self, assets, parent):
        self.assets = assets
        self.parent = parent
        self.surface = Surface(self.parent.get_size())

        #on redimensionne le background
        self.bg = transform.scale(assets['texs']['ig_bg'], parent.get_size())

        #0 = partie en cours
        #1 = pause
        #2 = perdu
        self.state = 0
        self.score = 0
        #délai en ms de chute
        self.fall = 250

        #curTetro: id du ttétro dans la liste tetrominos
        #startX/Y: coordonnées de démarrage
        #tetroX/Y: coordonnées du tétro
        #tetroHaut/Long: hauteur/largeur
        self.curTetro = -1
        self.startX = 2
        self.startY = 3
        self.tetroX = 0
        self.tetroY = 0
        self.tetroHaut = 0
        self.tetroLong = 0

        #paramètres de la grille
        self.tileSize = 25
        self.gridL = 22
        self.gridC = 10
        self.grid = Surface((self.gridC*self.tileSize, self.gridL*self.tileSize))

        #les briques solides
        self.wall = []
        for i in range(0,self.gridL+1):
            self.wall.append([])
            for j in range(0,self.gridC+1):
                self.wall[i].append(color[0])

        self.txtFont = Font(assets['fonts']['FORCED SQUARE'], 30)
        self.statFont = Font(assets['fonts']['FORCED SQUARE'], 20)
        #on fait le rendu du texte affiché avant de jouer, histoire de ne pas
        #gaspiller de ressources inutilement
        self.txtDisp = []

        for i in scoreData:
            num = scoreData.index(i)+1
            lignesTxt = "LIGNE"
            if num > 1:
                lignesTxt = "LIGNES"
            render = self.txtFont.render("{0} {1} = {2}".format(num, lignesTxt, i), 1, (0,0,0))
            self.txtDisp.append(render)

        self.txtDisp.append(self.txtFont.render("+1 PAR PIÈCE", 1, (0,0,0)))

        with open('save.game', 'rb') as f:
            cnt = pickle.load(f)
            self.nbPart = cnt[0]
            self.nbLoss = cnt[1]

        #stocker dans des listes nous permet d'utiliser des boucles facilement
        self.statVar = [self.nbPart, self.nbLoss, 0, 0]
        self.statIcon = []
        for i in statData: #définie dans utils
            self.statIcon.append(transform.scale(self.assets['texs'][i], (32,32)))

        self.renderPause()
        self.renderOver()

        set_timer(FALLDOWN, self.fall)

    def renderPause(self):
        self.pauseSurf = Surface(self.parent.get_size())

        self.pauseBg = transform.scale(self.assets['texs']['pause_bg'], self.parent.get_size())

        pause1 = self.txtFont.render('---PAUSE---', 1, (255,255,255))
        pause2 = self.txtFont.render('APPUYEZ SUR [Esc] POUR REPRENDRE LA PARTIE', 1, (255,255,255))

        cx = self.surface.get_width()/2
        cy = self.surface.get_height()

        self.pauseSurf.blit(self.pauseBg, (0,0))
        self.pauseSurf.blit(pause1, (cx-pause1.get_width()/2, cy/2-100))
        self.pauseSurf.blit(pause2, (cx-pause2.get_width()/2, cy/2-50))

    def renderOver(self):
        self.overSurf = Surface(self.parent.get_size())

        over = self.txtFont.render('GAME OVER', 1, (255,255,255))

        self.overSurf.fill((80,80,80))
        self.overSurf.blit(over, over.get_rect(center=self.overSurf.get_rect().center))

    #on recalcule la longueur en fonction de la rotation
    def recalcTetro(self):
            self.tetroHaut = 1
            self.tetroLong = 1
            for k in self.tetroForm:
                if k[0]+1 > self.tetroLong:
                    self.tetroLong = k[0]+1
                if k[1]+1 > self.tetroHaut:
                    self.tetroHaut = k[1]+1

    #création d'un nouveau tétromino
    def newTetro(self):
            self.curTetro = randint(0,6)
            self.tetroRot = randint(0,len(tetrominos[self.curTetro])-1)
            self.tetroForm = tetrominos[self.curTetro][self.tetroRot]
            self.tetroCol = color[randint(1,6)]
            self.tetroX = self.startX
            self.tetroY = self.startY
            self.recalcTetro()
            stLog('INFO', 'new tetro: long={0} haut={1} id={2}'.format(self.tetroLong, self.tetroHaut, self.curTetro))

    #ajouter le tétromino au "wall" + supprimer les lignes pleines
    def addToWall(self):
        if self.tetroX <= 3:
            #game over! :(
            with open('save.game', 'rb') as f:
                old = pickle.load(f)
                old[1] += 1
                if self.score > old[2]:
                    old[2] == self.score
                with open('save.game', 'wb') as f2:
                   pickle.dump(old, f2)
            self.state = 2
        else:
            self.score += 1
            for k in self.tetroForm:
                self.wall[k[1]+self.tetroX-self.tetroHaut+1][k[0]+self.tetroY] = self.tetroCol
            lines2delete = []
            for i in self.wall:
                compte = 1 #nombre de cases remplies dans la ligne
                for j in i:
                    if j: compte += 1
                if compte == len(i):
                    lines2delete.append(self.wall.index(i))

            for i in lines2delete:
                del self.wall[i]
                #on décale toutes les valeurs dans l'autre sens
                self.wall = [self.wall[-1]] + self.wall[:-1]

                #ligne vide à ajouter
                lineAdd = []
                for j in range(0,self.gridC+1):
                    lineAdd.append(color[0])

                self.wall.append(lineAdd)

            self.statVar[2] += len(lines2delete)
            if len(lines2delete) == 1: self.score += 200
            elif len(lines2delete) == 2: self.score += 1000
            elif len(lines2delete) == 3: self.score += 3000
            elif len(lines2delete) == 4:
                self.score += 10000
                self.statVar[3] += 1

            self.curTetro = -1

    def evManager(self, event):
        if event.type == KEYDOWN:
            if event.key == 27: #esc
                if self.state == 0:
                    set_timer(FALLDOWN, 0)
                    self.state = 1
                elif self.state == 1:
                    set_timer(FALLDOWN, self.fall)
                    self.state = 0
                elif self.state == 2: post(Event(GS_SWITCH, {'state': sys.modules['gs.menu'].MenuState}))
            elif event.key == 276: #left
                if self.tetroY > 0:
                    if self.wall[self.tetroX][self.tetroY-1] == None:
                        self.tetroY -= 1
            elif event.key == 275: #right
                if self.tetroY+self.tetroLong < self.gridC:
                    if self.wall[self.tetroX][self.tetroY+self.tetroLong] == None:
                        self.tetroY += 1
            elif event.key == 273: #up
                #si on ne dépasse pas la liste des rotations possibles
                if self.tetroRot+1 < len(tetrominos[self.curTetro]):
                    self.tetroRot += 1
                else:
                    self.tetroRot = 0
        elif event.type == FALLDOWN:
            wall = 0
            if self.tetroX+1 < self.gridL:
                for k in self.tetroForm:
                    if self.wall[self.tetroX+k[1]+1-self.tetroHaut+1][self.tetroY+k[0]]:
                        wall = 1
                        break
            else: wall = 1
            if wall:
                self.addToWall()
            else:
                self.tetroX += 1

    def draw(self):
        if self.state == 1:
            self.surface.blit(self.pauseSurf, (0,0))
        elif self.state == 2:
            self.surface.blit(self.overSurf, (0,0))
        elif self.state == 0:
            if self.curTetro == -1: self.newTetro()

            #on actualise si la rotation a changée
            if self.tetroForm != tetrominos[self.curTetro][self.tetroRot]:
                self.tetroForm = tetrominos[self.curTetro][self.tetroRot]
                self.recalcTetro()

            #on change la position si on dépasse de la grille
            if self.tetroY+self.tetroLong > self.gridC:
                self.tetroY -= self.tetroY+self.tetroLong-self.gridC

            self.grid.fill((80,80,80))
            self.surface.blit(self.bg, (0,0))

            scoreTxt = self.txtFont.render('SCORE: {0}'.format(self.score), 1, (0,0,0))
            txtSpce = 30
            #les info à gauche
            for i in self.txtDisp:
                ind = self.txtDisp.index(i)
                self.surface.blit(i, (120, 200+txtSpce*ind))

            #les stats
            for i in range(0,4):
                #position calculée en fonction de la taille de l'écran
                longPos = self.surface.get_width()-300
                self.surface.blit(self.statIcon[i], (longPos-5, 170+(txtSpce+10)*i))
                item = self.statFont.render("{0}: {1}".format(statInfo[i], self.statVar[i]), 1, (0,0,0))
                self.surface.blit(item, (longPos+40, 180+(txtSpce+10)*i))

            self.surface.blit(scoreTxt, (120,170))

            #grid
            for i in range(0, self.gridL):
                for j in range(0, self.gridC):
                    posX = j*self.tileSize
                    posY = i*self.tileSize
                    posCol = (255,255,255)
                    posFill = 1
                    if i == self.tetroX and j == self.tetroY: #si il s'agit de la place du tetromino
                        #utilisé pour dessiner les pièces au dessus de tetroX/Y
                        addX = j
                        addY = i+1
                        for k in self.tetroForm:
                            x_pos = (k[0]+addX)*self.tileSize
                            y_pos = (k[1]+addY-self.tetroHaut)*self.tileSize
                            #left, top, puis taille du carré
                            pos = [x_pos, y_pos, self.tileSize, self.tileSize]
                            rect(self.grid, self.tetroCol, pos, 0)
                            rect(self.grid, posCol, pos, 1)
                    if self.wall[i][j] != None:
                        posCol = self.wall[i][j]
                        posFill = 0

                    rect(self.grid, posCol, [posX, posY, self.tileSize, self.tileSize], posFill)

            self.surface.blit(self.grid, self.grid.get_rect(center=self.surface.get_rect().center))

