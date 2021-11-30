from os import path
from enum import Enum, auto
from locals import *
import pygame
from abc import ABC

"""
Responsible for modeling (and temporary for rendering!) of the game field and the player

Classes:
    
    CellType(Enum)
    Tower
    Player
    
Functions:
    
    square(screen, color, center, a) -> None

"""

def square(screen:pygame.Surface, color: tuple[int, int, int], center: tuple[int,int], a) -> None:
    """ Blits square and its border with given parameters onto given surface
    :param  screen: PyGame surface to blit square onto
    :param color: Color (R, G, B) of the square
    :param center: List (x, y) of the square's center
    :param a: Side length
    """
    x, y = center
    pygame.draw.rect(screen, color, (x - a / 2, y - a / 2, a, a))
    pygame.draw.rect(screen, Color.CITRINE, (x - a / 2, y - a / 2, a, a), 1)


class Cell(Enum):
    """ Describes all possible cell types """

    WALL = auto()
    SPIKE = auto()
    HOLE = auto()
    TREASURE = auto()
    EMPTY = auto()

class Tower:
    """ Stores all cells, manipulates and renders them """

    WIDTH = 13
    HEIGHT = 15

    def __init__(self):
        """ Initializes tower with data from field.txt file """
        dump = open(path.join('resources', 'field.txt'), "r").readlines()
        self.cells = ([
            [Cell.WALL if cell == "#" else Cell.EMPTY for cell in line]
            for line in dump])
        self.level = 0

    def move_floor(self, amount) -> None:
        """  Moves tower any amount of cells down
        :param amount: The amoutn of cells to raise the level by
        :return: None
        """
        self.level += amount

    def is_inside(self, pos: tuple[int, int]) -> bool:
        """ :returns: True if pos is a valid cell """
        x, y = pos
        return 0 <= x and x <= Tower.WIDTH

    def is_empty(self, pos: tuple[int, int]) -> bool:
        """ :returns: True if player can stay in the cell """
        x, y = pos
        return self.is_inside(pos) and self.cells[y % len(self.cells[0])][x] is Cell.EMPTY

    def update(self) -> None:
        """ For now tower has no animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """ """
        if event.type == pygame.KEYDOWN:
            self.move_floor(1)

    @staticmethod
    def calc_center(pos:tuple[int, int]) -> tuple[int, int]:
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
        a = 0.8 * HEIGHT / Tower.HEIGHT
        for i in range(Tower.HEIGHT):
            for j in range(Tower.WIDTH):
                color = Color.DEEP_BLUE if self.cells[(i + self.level) % len(self.cells[0])][j] is Cell.WALL else Color.BLACK
                square(screen, color, Tower.calc_center((i, j)), a)

class Player:
    """ Responsible for player moving, rendering """

    def __init__(self, tower:Tower):
        """ Initializes starting position """
        self.x, self.y = Tower.WIDTH // 2, 3
        self.tower = tower

    def move(self, dx, dy) -> None:
        """ Moves player if possible """
        new_x, new_y = self.x + dx, self.y + dy
        if self.tower.is_empty((new_x, new_y)):
            self.x = self.x + dx
            self.y = self.y + dy

    def update(self) -> None:
        """ For now tower has no animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles WASD movement
        :param event: Event to be handled, should be of KEYDOWN type """
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_w:
            self.move(0, 1)
        elif event.key == pygame.K_s:
            self.move(0, -1)
        elif event.key == pygame.K_a:
            self.move(-1, 0)
        elif event.key == pygame.K_d:
            self.move(1, 0)

    def render(self, screen: pygame.Surface) -> None:
        """
        :param screen: pygame surface to blit image on """
        a = 0.8 * HEIGHT / Tower.HEIGHT
        square(screen, Color.MAGENTA, Tower.calc_center((self.y - self.tower.level, self.x)), a)
    
    def is_alive(self) -> bool:
        """:returns: True if player is still visible """
        return self.y >= self.tower.level



if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    tower = Tower()
    player = Player(tower)
    abilitybar = AbilityBar(player)

    abilitybar.set_ability(0, KnightLeftUp(player))
    abilitybar.set_ability(1, KnightUpLeft(player))
    abilitybar.set_ability(2, KnightUpRight(player))
    abilitybar.set_ability(3, KnightRightUp(player))

    dynamic_elements = [tower, player, abilitybar]

    clock = pygame.time.Clock()
    finished = False

    # Main cycle
    while not finished:
        clock.tick(60)
        # Handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            else:
                for element in dynamic_elements:
                    element.handle(event)

        for element in dynamic_elements:
            element.update()
            element.render(screen)

        # Updates screen
        pygame.display.update()
        screen.fill(Color.BLACK)
    pygame.quit()
