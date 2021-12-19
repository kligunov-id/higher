import pygame
from random import choice
from locals import *
from chunks import ctype_by_letter
from spritesheet import SpriteSheet
import os

"""
Responsible for modeling and rendering of the game field and the player

Classes:
    
    Cell
    Tower
    Player
    
Functions:
    
    square(screen, color, center, a) -> None

"""


def square(screen: pygame.Surface, color: tuple[int, int, int], center: tuple[int, int], a: int) -> None:
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
    """ Stores the cell image and the type.
    Designed to be created with the Tower.load_chunk() function"""

    def __init__(self, size, ctype, image):
        """
        initiates the cell.
        :param size: Dimensions (width, height) of the cell
        :param ctype: Cell type: W for wall, H for hole and N for nothing, or an empty tile
        :param image: the image of the cell
        """
        self.size = size  # Currently unused, but may be usefull in future
        self.celltype = ctype
        self.image = pygame.transform.scale(image, size)

    def render(self) -> pygame.Surface:
        """:return: PyGame surface with the cell image"""
        return self.image

    def is_empty(self) -> bool:
        return self.celltype == 'N'

    def is_walkable(self) -> bool:
        return self.celltype == 'N' or self.celltype == 'H'


class Tower:
    """ Stores and loads from file all cells, stores player """
    WIDTH = 13
    HEIGHT = 15

    def __init__(self):
        """ Initializes tower with data from field.txt file """
        self.spritesheet = SpriteSheet('towersheet.png')
        self.cells = []
        self.level = 0  # level of the floor of the tower
        self.loaded_level = 0  # level of the highest loaded cell
        self.load_chunk(os.path.join('resources', 'chunks', '0_0.txt'))

        self.player = Player()

    def move_floor(self, amount=1) -> None:
        """ Moves tower any amount of cells down
        :param amount: The amount of cells to raise the level by
        """
        self.level += amount

    def get_chunk_path(self) -> str:
        """
        Randomly chooses chunk with difficulty based on tower level
        :return: Chunk file path
        """
        if self.level <= 40:
            difficulty = '0'
        elif self.level <= 120:
            difficulty = '1'
        else:
            difficulty = '2'

        chunkname = choice(os.listdir(os.path.join('resources', 'chunks', difficulty)))
        return os.path.join('resources', 'chunks', difficulty, chunkname)

    def load_chunk(self, chunk_path='') -> None:
        """ Loads chunk from a prepared(see chunks.py) file
        :param chunk_path: optional, use if you want to load a specific chunk by path
        """
        if not chunk_path:
            chunk_path = self.get_chunk_path()
        dump = open(chunk_path, 'r').readlines()
        dump.reverse()
        newcells = []
        a = int(0.8 * HEIGHT / Tower.HEIGHT)
        for n, line in enumerate(dump):
            newcells.append([])
            for sym in line.strip():
                newcells[n].append(Cell((a, a), ctype_by_letter[sym][0], self.spritesheet.image_at(ctype_by_letter[sym][1])))
        self.cells = self.cells + newcells
        self.loaded_level += len(dump)

    @staticmethod
    def is_inside(pos: tuple[int, int]) -> bool:
        """
        :param pos: (x, y) of a cell
        :return: True if pos is a valid cell
        """
        x, y = pos
        return 0 <= x <= Tower.WIDTH

    def is_empty(self, pos: tuple[int, int]) -> bool:
        """
        :param pos: (x, y) of a cell
        :return: True if player can stay in the cell
        """
        x, y = pos
        return self.is_inside(pos) and self.cells[y][x].is_empty()

    def is_walkable(self, pos: tuple[int, int]) -> bool:
        """
        :param pos: (x, y) of a cell
        :return: True if player can walk on the cell(if the cell is empty, or if the cell is a hole)
        """
        x, y = pos
        return self.is_inside(pos) and self.cells[y][x].is_walkable()

    def update(self) -> None:
        """Unpacks new chunks when the loaded amount gets too small"""
        if self.loaded_level <= self.level + 20:
            self.load_chunk()
        self.player.update()

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles events, dropping the tower 1 floor every button press
        :param event: PyGame event to be handled
        """
        if event.type == pygame.KEYDOWN:
            self.move_floor()
            self.player.handle(self, event)

    @staticmethod
    def calc_center(pos: tuple[int, int]) -> tuple[int, int]:
        """ Calculates on-screen position of an object based on index position in tower
        :param pos: Pair (i, j) of indices in tower
        """
        i, j = pos
        a = 0.8 * HEIGHT / Tower.HEIGHT
        x = WIDTH / 2 + (j - Tower.WIDTH / 2 + 1 / 2) * a
        y = (Tower.HEIGHT - 1 - i) * a
        return x, y

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
        self.player.render(screen, self.level)

    def move_sequence(self, *steps) -> None:
        """
        moves the player a sequence of steps
        :param steps: a list of (dx, dy) of movements
        """
        self.player.move_sequence(self, *steps)

    def is_player_alive(self) -> bool:
        """ :return: True if player is alive """
        return self.player.is_alive(self.level)

class Player:
    """Responsible for player movement, rendering"""

    def __init__(self):
        """
        Initializes starting position
        :param tower: the Tower object inside which the player is located
        """
        self.x, self.y = Tower.WIDTH // 2, 3

    def move(self, tower: Tower, pos: tuple[int, int], step: tuple[int, int]) -> tuple[int, int]:
        """
        Calculates movement from a given position in a given tower
        :param tower: Tower inside which the player is moving
        :param pos: (x,y) of a cell
        :param step: (dx, dy) of a single movement
        :return: (x, y) of the cell after the movement
        """
        new_x, new_y = pos[0] + step[0], pos[1] + step[1]
        if tower.is_walkable((new_x, new_y)):
            return new_x, new_y
        return pos

    def move_sequence(self, tower: Tower, *steps) -> None:
        """
        moves the player a sequence of steps
        :param tower: Tower inside which the player is moving
        :param steps: a list of (dx, dy) of movements
        """
        new_pos = (self.x, self.y)
        for step in steps:
            new_pos = self.move(tower, new_pos, step)
            if tower.is_empty(new_pos):
                self.x, self.y = new_pos

    def update(self) -> None:
        """ For now player has no animation or progression """
        pass

    def handle(self, tower:Tower, event: pygame.event.Event) -> None:
        """
        Handles WASD movement
        :param tower: Tower inside which the player is moving
        :param event: Event to be handled, should be of KEYDOWN type
        """
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_w:
            self.move_sequence(tower, (0, 1))
        elif event.key == pygame.K_s:
            self.move_sequence(tower, (0, -1))
        elif event.key == pygame.K_a:
            self.move_sequence(tower, (-1, 0))
        elif event.key == pygame.K_d:
            self.move_sequence(tower, (1, 0))

    def render(self, screen: pygame.Surface, level: int = 0) -> None:
        """
        renders self onto a screen
        :param screen: pygame surface to blit image on
        :param level: Level of the tower the player is climbing
        """
        a = 0.8 * HEIGHT / Tower.HEIGHT
        square(screen, Color.MAGENTA, Tower.calc_center((self.y - level, self.x)), a)

    def is_alive(self, level: int) -> bool:
        """
        :param level: Level of the tower the player is climbing
        :return: True if player is still visible """
        return self.y >= level


if __name__ == '__main__':
    print("this module is for describing the functions and classes of the game 'Higher', it's not supposed to be "
          "launched directly. To learn more about the game, visit https://github.com/kligunov-id/higher")
