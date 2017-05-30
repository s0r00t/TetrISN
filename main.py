#!/usr/bin/env python3
from gs.menu import MenuState
from pygame.locals import *
from utils import *
import os
import pickle
import pygame as pyg
import sys

class TetrISN():
    def __init__(self):
        self.assets = {}
        self.assets['fonts'] = {}
        self.assets['texs'] = {}
        if not os.path.isfile('save.game'):
            stLog('INFO', 'Creating savefile...')
            with open('save.game', 'wb') as f:
                pickle.dump([int(),int(),int()], f)

        pyg.init()
        pyg.mouse.set_visible(0)
        self.screen = pyg.display.set_mode((0,0))
        
        self.loadAssets()
        
        pyg.display.set_caption('TetrISN')
        pyg.display.set_icon(self.assets['texs']['icon'])
        
        self.gs = MenuState(self.assets, self.screen)
        self.mainLoop()

    def loadAssets(self):
        logLoad = '???'
        for subdir, dirs, files in os.walk('assets'):
            for file in files:
                name = os.path.splitext(file)[0]
                path = os.path.join(subdir, file)
                if file.endswith('.ttf'):
                    logLoad = 'font'
                    self.assets['fonts'][name] = path
                elif file.endswith('.png'):
                    logLoad = 'tex'
                    self.assets['texs'][name] = pyg.image.load(path).convert_alpha()

                stLog('INFO', '{0}: loaded {1} ({2})'.format(logLoad, name, path))

    def evManager(self):
        for ev in pyg.event.get():
                if ev.type == QUIT:
                    sys.exit()
                elif ev.type == GS_SWITCH:
                    stLog('INFO', 'Switching to GS "{0}"'.format(ev.state.__name__))
                    self.gs = ev.state(self.assets, self.screen)
                else:
                    self.gs.evManager(ev)

    def mainLoop(self):
        while True:
                self.evManager()
                self.gs.draw()
                self.screen.blit(self.gs.surface, (0,0))
                pyg.display.flip()

if __name__ == '__main__':
    try:
        TetrISN()
    except KeyboardInterrupt:
        stLog('FATAL', 'Ctrl-C detected. Shutting down.')
        sys.exit(1)

