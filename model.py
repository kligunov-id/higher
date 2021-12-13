import random
from os import path
from enum import Enum, auto
from locals import *
from chunks import *
import pygame
from math import ceil
from abc import ABC
from spritesheet import *

"""
Responsible for modeling (and temporary for rendering!) of the game field and the player

Classes:
    
    CellType(Enum)
    Tower
    Player
    
Functions:
    
    square(screen, color, center, a) -> None

"""


def square(screen: pygame.Surface, color: tuple[int, int, int], center: tuple[int, int], a) -> None:
    """ Blits square and its border with given parameters onto given surface
    :param  screen: PyGame surface to blit square onto
    :param color: Color (R, G, B) of the square
    :param center: List (x, y) of the square's center
    :param a: Side length
    """
    x, y = center
    pygame.draw.rect(screen, color, (x - a / 2, y - a / 2, a, a))
    pygame.draw.rect(screen, Color.CITRINE, (x - a / 2, y - a / 2, a, a), 1)


class Cell:
    """ Describes all possible cells, stores the cell image and it's type """

    def __init__(self, size, spritesheet, tup):
        self.celltype = tup[0]
        self.image = pygame.transform.scale(spritesheet.image_at(tup[1]), size)

    def render(self):
        return self.image


class Tower:
    """ Stores all cells, manipulates and renders them """
    WIDTH = 13
    HEIGHT = 15

    def __init__(self):
        """ Initializes tower with data from field.txt file """
        self.spritesheet = SpriteSheet('towersheet.png')
        self.cells = []
        self.player = Player(self)
        self.level = 0  # level of the floor of the tower
        self.loaded_level = 0  # level of the highest loaded cell
        self.load_chunk(0, '0_0.txt')

    def move_floor(self, amount=1) -> None:
        """  Moves tower any amount of cells down
        :param amount: The amount of cells to raise the level by
        :return: None
        """
        self.level += amount

    def get_chunk_name(self, level: int):
        """
        generates a name for a chunk to be generated from the level the tower is on
        the name is built by combining the difficulty and a random id for the chunk
        :param level: the level of the tower (to get the appropriate difficulty from)
        """
        if level <= 20:
            difficulty = 0
        elif level <= 80:
            difficulty = 1
        else:
            difficulty = 2
        ID = random.randint(1, 10)
        return str(difficulty) + "_" + str(ID) + ".txt"

    def load_chunk(self, level, chunk_name='') -> None:
        """loads chunk from a prepared(see chunks.py) file
        :param level: level of the tower, passed to get_chunk_name
        :param chunk_name: optional, use if you want to load a specific chunk by name
        """
        if not chunk_name:
            chunk_name = self.get_chunk_name(level)
        dump = open(path.join('resources', 'chunks', chunk_name + '_refactored.txt'), 'r').readlines()
        dump.reverse()
        newcells = []
        a = int(0.8 * HEIGHT / Tower.HEIGHT)
        for n, line in enumerate(dump):
            newcells.append([])
            for sym in line.strip():
                newcells[n].append(Cell((a, a), self.spritesheet, slovar2[sym]))
        self.cells = self.cells + newcells
        self.loaded_level += len(dump)

    def is_inside(self, pos: tuple[int, int]) -> bool:
        """
        :param pos: (x, y) of a cell
        :returns: True if pos is a valid cell
        """
        x, y = pos
        return 0 <= x and x <= Tower.WIDTH

    def is_empty(self, pos: tuple[int, int]) -> bool:
        """
        :param pos: (x, y) of a cell
        :returns: True if player can stay in the cell
        """
        x, y = pos
        return self.is_inside(pos) and self.cells[y][x].celltype == 'N'

    def is_walkable(self, pos: tuple[int, int]) -> bool:
        """
        :param pos: (x, y) of a cell
        :returns: True if player can walk on the cell(if the cell is empty, or if the cell is a hole)
        """
        x, y = pos
        return self.is_inside(pos) and self.cells[y][x].celltype == 'N' or self.cells[y][x].celltype == 'H'

    def update(self) -> None:
        """Unpacks new chunks when the loaded amount gets too small"""
        if self.loaded_level <= self.level + 20:
            self.load_chunk(self.level)

    def handle(self, event: pygame.event.Event) -> None:
        """Handles events, dropping the tower 1 floor every button press
        :param event: a pygame.Event to be handled
        """
        if event.type == pygame.KEYDOWN:
            self.player.handle(event)
            self.move_floor()

    @staticmethod
    def calc_center(pos: tuple[int, int]) -> tuple[int, int]:
        """ Calculates on-screen position of an object based on index position in tower
        :param pos: Pair (i, j) of indices in tower
        """
        i, j = pos
        a = 0.8 * HEIGHT / Tower.HEIGHT
        x = WIDTH / 2 + (j - Tower.WIDTH / 2 + 1 / 2) * a
        y = (Tower.HEIGHT - 1 - i) * a
        return (x, y)

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders cells and the player onto a surface
        :param screen: pygame surface to blit image on
        """
        a = int(0.8 * HEIGHT / Tower.HEIGHT)
        level = int(self.level)
        for i in range(level, level + Tower.HEIGHT):
            for j in range(Tower.WIDTH):
                pos = (Tower.calc_center((i - level, j))[0] - a / 2, Tower.calc_center((i - level, j))[1] - a / 2)
                screen.blit(self.cells[i][j].render(), pos)
        self.player.render(screen)


class Player:
    """Responsible for player movement, rendering"""

    def __init__(self, tower: Tower):
        """
        Initializes starting position
        :param tower: the Tower object inside which the player is located
        """
        self.x, self.y = Tower.WIDTH // 2, 3
        self.tower = tower

    def move(self, pos, step) -> tuple[int, int]:
        """
        Calculates movement from a given position
        :param pos: (x,y) of a cell
        :param step: (dx, dy) of a single movement
        :return: (x, y) of the cell after the movement
        """
        new_x, new_y = pos[0] + step[0], pos[1] + step[1]
        if self.tower.is_walkable((new_x, new_y)):
            return (new_x, new_y)
        return pos

    def move_sequence(self, *steps) -> None:
        """
        moves the player a sequence of steps
        :param steps: a list of (dx, dy) of movements
        :return: None
        """
        new_pos = (self.x, self.y)
        for step in steps:
            new_pos = self.move(new_pos, step)
            if self.tower.is_empty(new_pos):
                self.x, self.y = new_pos

    def update(self) -> None:
        """ For now player has no animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """
        Handles WASD movement
        :param event: Event to be handled, should be of KEYDOWN type
        """
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_w:
            self.move_sequence((0, 1))
        elif event.key == pygame.K_s:
            self.move_sequence((0, -1))
        elif event.key == pygame.K_a:
            self.move_sequence((-1, 0))
        elif event.key == pygame.K_d:
            self.move_sequence((1, 0))

    def render(self, screen: pygame.Surface) -> None:
        """
        renders self onto a screen
        :param screen: pygame surface to blit image on
        """
        a = 0.8 * HEIGHT / Tower.HEIGHT
        square(screen, Color.MAGENTA, Tower.calc_center((self.y - self.tower.level, self.x)), a)

    def is_alive(self) -> bool:
        """:returns: True if player is still visible """
        return self.y >= self.tower.level


if __name__ == '__main__':
    print("wherefore has't thee did summon me m'rtal, art thee not acknown yond i'm not the main module?")
