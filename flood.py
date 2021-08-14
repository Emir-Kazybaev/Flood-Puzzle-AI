import sys
import pygame as pg
import pygame.time

from constants import HEIGHT, WIDTH, BACK, BFS, ASTAR, DES, BFSplus, NEWGAME, NEXT, RGB_COLOR_DIC, COLORS
from random import randint
from node import Node
from solver import Solver


def dict_of_colors(node):
    color_dictionary = {}
    for i in node.grid:
        if i not in color_dictionary:
            color_dictionary[i] = 0
        color_dictionary[i] += 1
    color_dictionary[node.grid[0]] -= len(node.filled_indexes)
    return color_dictionary


class Flood:
    def __init__(self, side_length, num_of_colors):
        self.SIDE_LENGTH = side_length
        self.NUM_OF_COLORS = num_of_colors
        self.CELL_SIZE = int(HEIGHT / self.SIDE_LENGTH)
        pg.init()
        pg.display.set_caption('Flood Puzzle by K. Emir')
        self.FONT_1 = pg.font.SysFont("Comic Sans MS", 30)
        self.FONT_2 = pg.font.SysFont('comicsans', 60)
        self.SCREEN = pg.display.set_mode([WIDTH, HEIGHT])
        self.FPS = 60
        self.cursor = 0
        self.nodes = []

    def update_screen(self):
        self.SCREEN.fill(RGB_COLOR_DIC['gray'])
        for i in range(self.SIDE_LENGTH):
            for j in range(self.SIDE_LENGTH):
                if i * self.SIDE_LENGTH + j in self.nodes[self.cursor].filled_indexes:
                    color = self.nodes[self.cursor].color
                else:
                    color = self.nodes[self.cursor].grid[i * self.SIDE_LENGTH + j]
                pg.draw.rect(self.SCREEN, RGB_COLOR_DIC[color],
                             pg.Rect(j * self.CELL_SIZE, i * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
        pg.draw.rect(self.SCREEN, (140, 142, 142), pg.Rect(self.CELL_SIZE * self.SIDE_LENGTH, 0, 10, HEIGHT))
        steps = self.FONT_1.render("Steps : " + str(self.cursor), 1, RGB_COLOR_DIC['black'])
        self.SCREEN.blit(steps, (820, 10))
        self.SCREEN.blit(BACK, (800, 50))
        self.SCREEN.blit(NEXT, (900, 50))
        self.SCREEN.blit(ASTAR, (835, 130))
        self.SCREEN.blit(BFSplus, (835, 280))
        self.SCREEN.blit(DES, (835, 430))
        self.SCREEN.blit(BFS, (835, 580))
        self.SCREEN.blit(NEWGAME, (800, 670))
        pg.display.update()

    def generate_grid(self):
        if 0 < self.NUM_OF_COLORS <= 10:
            if 3 <= self.SIDE_LENGTH <= 200:
                grid = []
                for i in range(self.SIDE_LENGTH * self.SIDE_LENGTH):
                    grid.append(COLORS[randint(0, self.NUM_OF_COLORS - 1)])
                return grid

    def handle_click(self, click):
        if click[0] < self.CELL_SIZE * self.SIDE_LENGTH:
            index = click[1] // self.CELL_SIZE * self.SIDE_LENGTH + click[0] // self.CELL_SIZE
            return self.nodes[self.cursor].grid[index]
        elif 70 < click[1] < 125:
            if 800 < click[0] < 900:
                if self.cursor != 0:
                    self.cursor -= 1
            else:
                if self.cursor < len(self.nodes) - 1:
                    self.cursor += 1
        elif 140 < click[1] < 265:
            self.solve(2)
        elif 290 < click[1] < 415:
            self.solve(1)
        elif 440 < click[1] < 565:
            self.solve(3)
        elif 590 < click[1] < 715:
            self.solve(0)
        elif 750 < click[1] < 800:
            self.start_flood()
        else:
            return None

    def show_solution(self):
        start = self.cursor
        for i in range(self.cursor, len(self.nodes)):
            self.cursor = i
            self.update_screen()
            pygame.time.delay(125)
        pygame.time.delay(1000)
        self.cursor = start

    def solve(self, method_num):
        solver = Solver(self.nodes[self.cursor])
        if method_num == 2:
            solution = solver.a_star()
        elif method_num == 1:
            solution = solver.optimized_bfs()
        elif method_num == 0:
            solution = solver.bfs()
        elif method_num == 3:
            solution = solver.des()
        else:
            print("Wrong method number!")
            solution = []
        self.nodes = self.nodes[:self.cursor + 1] + solution[0]
        print(f"Moves: {solution[1]}, Time: {solution[2]}, Nodes Explored: {solution[3]}, Path: {solution[4]}")
        self.show_solution()
        return solution[1], solution[2], solution[3]

    def end_screen(self):
        text = "Puzzle solved in " + str(len(self.nodes) - 1) + " moves."
        draw_text = self.FONT_2.render(text, 1, RGB_COLOR_DIC['w'])
        self.SCREEN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2 - 100, HEIGHT / 3))
        pg.display.update()
        pg.time.delay(3000)
        self.start_flood()

    def setup_start_node(self, grid):
        node = Node(None, grid, grid[0], self.SIDE_LENGTH, 0,
                    {'g': -1, 'b': -1, 'r': -1, 'y': -1, 'o': -1, 'p': -1, 'w': -1, 'black': -1, 'gray': -1, 'c': -1}, set(), set([0]), set())
        node.start_coloring(grid[0])
        node.colors_num = dict_of_colors(node)
        node.generate_id()
        self.cursor = 0
        self.nodes.clear()
        self.nodes.append(node)

    def start_flood(self):
        grid = self.generate_grid()
        print(grid)
        self.setup_start_node(grid)
        clock = pg.time.Clock()
        self.update_screen()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.nodes[self.cursor].solved():
                    self.end_screen()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    click = pg.mouse.get_pos()
                    color = self.handle_click(click)
                    if color is not None:
                        child = self.nodes[self.cursor].child_node()
                        if color != child.color:
                            child.start_coloring(color)
                            child.generate_id()
                            self.cursor += 1
                            self.nodes = self.nodes[:self.cursor] + [child]
                self.update_screen()
            clock.tick(self.FPS)
