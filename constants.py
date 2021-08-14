import pygame as pg
import os

HEIGHT = 800
WIDTH = 1000
COLORS = ['g', 'b', 'r', 'y', 'o', 'p', 'w', 'black','gray','c']

BACK_IMG = pg.image.load(os.path.join('Assets', 'BACK.png'))
BACK = pg.transform.scale(BACK_IMG, (100, 100))
NEXT_IMG = pg.image.load(os.path.join('Assets', 'NEXT.png'))
NEXT = pg.transform.scale(NEXT_IMG, (100, 100))
NEWGAME_IMG = pg.image.load(os.path.join('Assets', 'NEWGAME.png'))
NEWGAME = pg.transform.scale(NEWGAME_IMG, (200, 175))
BFS_IMG = pg.image.load(os.path.join('Assets', 'bfs.png'))
BFS = pg.transform.scale(BFS_IMG, (150, 150))
ASTAR_IMG = pg.image.load(os.path.join('Assets', 'astar.png'))
ASTAR = pg.transform.scale(ASTAR_IMG, (150, 150))
DES_IMG = pg.image.load(os.path.join('Assets', 'DES.png'))
DES = pg.transform.scale(DES_IMG, (150, 150))
BFSplus_IMG = pg.image.load(os.path.join('Assets', 'BFS+.png'))
BFSplus = pg.transform.scale(BFSplus_IMG, (150, 150))
RGB_COLOR_DIC = {'y': (255, 240, 0), 'o': (255, 170, 29), 'r': (255, 0, 127),
                 'g': (128, 187, 76), 'b': (25, 116, 210), 'p': (148, 99, 229),
                 'black': (0, 0, 0), 'w': (255, 255, 255), 'gray': (200, 200, 200), 'c': (8, 232, 222)}