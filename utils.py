from time import strftime
from pygame.event import Event
from pygame.locals import USEREVENT

class LogError(Exception): pass

#custom event to switch state
GS_SWITCH = USEREVENT + 1
#chute des pièces
FALLDOWN = USEREVENT + 2

#les pièces sont définies par 4 carrés
#ces carrés sont définis dans un repère orthonormé
#chaque rotation est prédéfinie

tBarre = [[(0,0),(0,1),(0,2),(0,3)], 
        [(0,0),(1,0),(2,0),(3,0)]]

tCarre = [[(0,0),(0,1),(1,0),(1,1)]]

tT = [[(0,1),(1,1),(1,0),(2,1)], 
        [(0,1),(1,1),(1,2),(1,0)],
        [(0,1),(1,1),(1,2),(2,1)],
        [(0,0),(0,1),(0,2),(1,1)]]  

tJ = [[(0,0),(1,0),(1,1),(1,2)],
        [(0,1),(0,2),(1,1),(2,1)],
        [(0,0),(0,1),(0,2),(1,2)],
        [(0,1),(1,1),(2,1),(2,0)]]

tL = [[(0,0),(0,1),(0,2),(1,0)],
        [(0,1),(0,2),(1,2),(2,2)],
        [(0,2),(1,2),(1,1),(1,0)],
        [(0,1),(1,1),(2,1),(2,2)]]

tS = [[(0,0),(1,0),(1,1),(2,1)],
        [(0,2),(0,1),(1,1),(1,0)]]

tZ = [[(0,1),(1,1),(1,0),(2,0)],
        [(0,0),(0,1),(1,1),(1,2)]]

tetrominos = [
        tBarre,
        tCarre,
        tT,
        tJ,
        tL,
        tS,
        tZ
]

color = [
        None, #rien
        (150,0,150), #violet
        (0,50,150), #bleu
        (0,150,0), #vert
        (200,200,0), #jaune
        (200,100,0), #orange
        (200,0,0) #rouge
]

#1, 2, 3 et 4 lignes
scoreData = [200, 1000, 3000, 10000]

statData = ["icon_heart", "icon_bheart", "icon_light", "icon_star"]
statInfo = ["NOMBRE DE PARTIES", "NOMBRE DE PERTES", "NOMBRE DE LIGNES", "NOMBRE DE TETRIS"]

#cette fonction nous permet de logger des messages importants
#dans la console de développement.
def stLog(type, msg):
    if type in ['INFO','WARN','ERROR','FATAL']:
        print(strftime("%H:%M:%S")+': [{0}] {1}'.format(type,msg))
    else:
        raise LogError("Erreur de log: {0}.".format(msg))
         
