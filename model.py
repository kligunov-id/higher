from os import path
from enum import Enum, auto
from locals import *
import pygame

"""
Responsible for modeling (and temporary for rendering!) of the game field and the player

Classes:
    
    CellType(Enum)
    Tower

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
    EMPTY = auto()

class Tower:
    """ Stores all cells, manipulates and renders them """

    WIDTH = 7
    HEIGHT = 7

    def __init__(self):
        """ Initializes tower with data from field.txt file """
        dump = open(path.join('resources', 'field.txt'), "r").readlines()
        self.cells = ([
            [Cell.WALL if cell == "#" else Cell.EMPTY for cell in line]
            for line in dump])
        self.level = 0

    def move_floor(self) -> None:
        """ Moves tower one block down """
        self.level += 1

    def is_inside(self, pos: tuple[int, int]) -> bool:
        pass

    def is_empty(self, pos: tuple[int, int]) -> bool:
        pass

    def update(self) -> None:
        """ For now tower has no animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """ """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.move_floor()

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

if __name__ == '__main__':
    print(Cell.WALL)
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    tower = Tower()
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
                tower.handle(event)

        tower.update()
        tower.render(screen)

        # Updates screen
        pygame.display.update()
        screen.fill(Color.BLACK)
    pygame.quit()
