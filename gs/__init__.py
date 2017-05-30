from pygame import Surface

#un GameState (ou GS) est un état de jeu :
#menu, en cours de partie, recherche réseau...
#chaque GS a son propre gestionnaire d'events (evManager)
#et sa propre surface qui est hiérarchisé sous screen


class GameState():
    def __init__(self, parent=None):
        self.surface = Surface(0,0)

    def evManager(self, event): pass

