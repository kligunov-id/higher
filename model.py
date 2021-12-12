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
        self.load_chunk('field.txt')
        self.level = 0

    def move_floor(self, amount=1) -> None:
        """  Moves tower any amount of cells down
        :param amount: The amoutn of cells to raise the level by
        :return: None
        """
        self.level += amount

    def load_chunk(self, chunk_name) -> None:
        """loads chunk from a prepared(see chunks.py) file"""
        dump = open(path.join('resources', 'chunks', chunk_name + '_refactored.txt'), 'r').readlines()
        dump.reverse()
        newcells = []
        a = int(0.8 * HEIGHT / Tower.HEIGHT)
        for n, line in enumerate(dump):
            newcells.append([])
            for sym in line.strip():
                newcells[n].append(Cell((a, a), self.spritesheet, slovar2[sym]))
        self.cells = self.cells + newcells

    def is_inside(self, pos: tuple[int, int]) -> bool:
        """:return: True if pos is a valid cell """
        x, y = pos
        return 0 <= x and x <= Tower.WIDTH

    def is_empty(self, pos: tuple[int, int]) -> bool:
        """:return: True if player can stay in the cell """
        x, y = pos
        return self.is_inside(pos) and self.cells[y][x].celltype == 'N'

    def is_walkable(self, pos: tuple[int, int]) -> bool:
        """:return: True if player can walk on the cell """
        x, y = pos
        return self.is_inside(pos) and self.cells[y][x].celltype == 'N' or self.cells[y][x].celltype == 'H'

    def update(self) -> None:
        """ For now tower has no animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """Handles events, dropping the tower 1 floor every button press"""
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
        """ Renders all tower cells 
        :param screen: pygame surface to blit image on """
        a = int(0.8 * HEIGHT / Tower.HEIGHT)
        level = int(self.level)#fixme
        for i in range(level, level + Tower.HEIGHT):
            for j in range(Tower.WIDTH):
                pos = (Tower.calc_center((i-level, j))[0]-a/2, Tower.calc_center((i-level, j))[1]-a/2)
                screen.blit(self.cells[i][j].render(), pos)
        self.player.render(screen)


class Player:
    """ Responsible for player moving, rendering """

    def __init__(self, tower: Tower):
        """ Initializes starting position """
        self.x, self.y = Tower.WIDTH // 2, 3
        self.tower = tower

    def move(self, pos, step) -> tuple[int, int]:
        """ Moves player if possible """
        new_x, new_y = pos[0] + step[0], pos[1] + step[1]
        if self.tower.is_walkable((new_x, new_y)):
            return (new_x, new_y)
        return pos

    def move_sequence(self, *steps):
        new_pos = (self.x, self.y)
        for step in steps:
            new_pos = self.move(new_pos, step)
            if self.tower.is_empty(new_pos):
                self.x, self.y = new_pos

    def update(self) -> None:
        """ For now tower has no animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles WASD movement
        :param event: Event to be handled, should be of KEYDOWN type """
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
        """:param screen: pygame surface to blit image on """
        a = 0.8 * HEIGHT / Tower.HEIGHT
        square(screen, Color.MAGENTA, Tower.calc_center((self.y - self.tower.level, self.x)), a)

    def is_alive(self) -> bool:
        """:returns: True if player is still visible """
        return self.y >= self.tower.level


if __name__ == '__main__':
    print("wherefore has't thee did summon me m'rtal, art thee not acknown yond i'm not the main module?")
