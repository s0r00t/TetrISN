from gs import GameState
from gs.ingame import IGState
from pygame import Surface, transform
from pygame.event import Event, post
from pygame.font import Font
from pygame.locals import HWSURFACE, KEYDOWN, SRCALPHA
from utils import *
from sys import exit
import pickle

class MenuState(GameState):
    def __init__(self, assets, parent):
        self.assets = assets
        self.parent = parent
        self.surface = Surface(parent.get_size())

        #resize background
        self.bg = transform.scale(assets['texs']['menu_bg'], parent.get_size())

        self.content = ['NOUVELLE PARTIE', 'QUITTER']
        self.itemColor = (0,0,0)
        self.itemPad = 30
        self.menuSelect = 0
        logoFont = Font(assets['fonts']['FORCED SQUARE'], 60)
        self.logo = logoFont.render('TetrISN', 1, (0,0,0))
        self.menuFont = Font(assets['fonts']['FORCED SQUARE'], 30)
        self.credits = self.menuFont.render('Antoine BOILEAU & Hugo COURTIAL, 2017', 1, (0,0,0))

        #temp arrow
        self.arrow = self.menuFont.render("->", 1, self.itemColor)

    def evManager(self, event):
        if event.type == KEYDOWN:
            if event.key == 273: #up
                if self.menuSelect > 0:
                    self.menuSelect -= 1
                else: 
                    self.menuSelect = len(self.content) -1
            elif event.key == 274: #down
                if self.menuSelect < len(self.content) - 1:
                    self.menuSelect += 1
                else:
                    self.menuSelect = 0
            elif event.key == 13: #enter
                choice = self.content[self.menuSelect]
                if choice == 'NOUVELLE PARTIE':
                    with open('save.game', 'rb') as f:
                        old = pickle.load(f)
                        old[0] += 1
                        with open('save.game', 'wb') as f2:
                            pickle.dump(old, f2)
                    
                    #on envoie un event GS_SWITCH pour changer de gs
                    post(Event(GS_SWITCH, {'state': IGState}))
                elif choice == 'QUITTER':
                    exit(0)
        
    def draw(self):
        halfScreenX = self.parent.get_width()/2
        halfScreenY = self.parent.get_height()/2
        menu = Surface((halfScreenX, halfScreenY), HWSURFACE | SRCALPHA)
        halfMenuX = menu.get_width()/2
        
        #background
        self.surface.blit(self.bg, (0,0))

        cx = self.surface.get_width()-self.credits.get_width()
        cy = self.surface.get_height()-(self.credits.get_height()*2)
        
        self.surface.blit(self.credits, (cx, cy)) 
        
        menu.blit(self.logo, (halfMenuX-self.logo.get_width()/2, 0))
        
        for i in self.content:
            item = self.menuFont.render(i, 1, self.itemColor)
            ix = halfMenuX-item.get_width()/2
            iy = 30+self.itemPad+self.itemPad*self.content.index(i)

            menu.blit(item, (ix, iy))

            if self.content[self.menuSelect] == i:
                menu.blit(self.arrow, (halfMenuX-200, iy)) 
       
        self.surface.blit(menu, menu.get_rect(center=self.surface.get_rect().center))

