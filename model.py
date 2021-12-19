import os.path
import pygame
from random import choice
from locals import *
from chunks import ctype_by_letter
from spritesheet import SpriteSheet

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
    """ Stores and loads from file all cells,  """
    WIDTH = 13  # the width of the tower in cells
    HEIGHT = 15  # the height of the tower in cells
    animtime = 4  # the amount of frames the movement animation takes

    def __init__(self):
        """ Initializes tower with data from field.txt file """
        self.spritesheet = SpriteSheet('towersheet.png')
        self.cells = []
        self.level = 0  # level of the floor of the tower
        self.target_level = 0 # level at which the tower should be when the animation is finished
        self.loaded_level = 0  # level of the highest loaded cell
        self.progress = 0  # an amount from 0 to animtime, how much the tower has progressed in animation
        self.load_chunk(os.path.join('resources', 'chunks', '0_0.txt'))
        self.cell_length = 0.8*HEIGHT/Tower.HEIGHT
        self.player = Player((self.cell_length, self.cell_length))

    def move_floor(self, amount=1) -> None:
        """ Moves tower any amount of cells down
        :param amount: The amount of cells to raise the level by
        """
        self.target_level += amount

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
        """Unpacks new chunks when the loaded amount gets too small, updates
        the level of the tower and updates player
        """
        if self.loaded_level <= self.level + 20:
            self.load_chunk()
        if self.level != self.target_level:
            self.level += (self.target_level-self.level)/(self.animtime-self.progress)
            self.progress +=1
            if self.progress == self.animtime:
                self.progress = 0
        self.player.update()

    def handle(self, event: pygame.event.Event) -> None:
        """Handles events, dropping the tower 1 floor every button press
        :param event: a pygame.Event to be handled
        """
        if event.type == pygame.KEYDOWN:
            self.move_floor()
            self.player.handle(self, event)

    @staticmethod
    def calc_center(pos: tuple[int, int]) -> tuple[int, int]:
        """ Calculates the position of a point relative to the tower
        :param pos: Pair (y, x) of coordinates of the point, measured in cells
        """
        y, x = pos
        a = 0.8 * HEIGHT / Tower.HEIGHT
        return (x+1/2) * a, 0.8*HEIGHT - (y+1/2) * a

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders cells and the player onto a surface
        :param screen: pygame surface to blit image on
        """
        level = int(self.level)
        surf = pygame.Surface((self.cell_length * self.WIDTH, self.cell_length * self.HEIGHT))
        for i in range(level-1, level + Tower.HEIGHT+1):
            for j in range(Tower.WIDTH):
                pos = (Tower.calc_center((i - self.level, j))[0] - self.cell_length / 2,
                       Tower.calc_center((i - self.level, j))[1] - self.cell_length / 2)
                surf.blit(self.cells[i][j].render(), pos)
        self.player.render(surf, self.level)
        screen.blit(surf, surf.get_rect(center = (WIDTH/2, 0.4 * HEIGHT)))

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

    def __init__(self, size: tuple[int, int]):
        """
        Initializes starting position
        :param size: the size (width, height) of the player on the screen
        """
        self.x, self.y = Tower.WIDTH // 2, 3
        self.size = size
        self.player_artist = PlayerArtist(self)

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
                self.player_artist.add_to_queue(new_pos)


    def update(self) -> None:
        """ Updates the player animation via the PlayerArtist class"""
        self.player_artist.update()

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

    def render(self, screen: pygame.Surface, level: float) -> None:
        """
        renders self onto a screen
        :param screen: pygame surface to blit image on
        """
        self.player_artist.render(screen, level)

    def is_alive(self, level: int) -> bool:
        """
        :param level: Level of the tower the player is climbing
        :return: True if player is still visible """
        return self.y >= level


class PlayerArtist():

    animtime = 4 # the amount of frames the movement animation takes

    def __init__(self, player):
        self.player = player
        self.pos = (player.x, player.y)
        self.progress = 0
        self.queue = []
        self.celllength = 0.8*HEIGHT/Tower.HEIGHT

        self.spritesheet = SpriteSheet('playersheet.png')
        self.frames = self.spritesheet.images_at([(180, 10, 160, 160), (350, 10, 160, 160)], Color.WHITE)
        for num, frame in enumerate(self.frames):
            self.frames[num] = pygame.transform.scale(frame, (self.celllength, self.celllength))
        self.rect = self.frames[0].get_rect()
        self.frame_number = 0

    def add_to_queue(self, pos):
        self.queue.append(pos)

    def switch_frame(self):
        self.frame_number = 1 - self.frame_number

    def update(self):
        if self.queue and self.pos == self.queue[0]:
            self.queue.pop(0)
            self.progress = 0
            if not self.queue:
                self.switch_frame()

        if self.queue:
            self.pos = (self.pos[0] + (self.queue[0][0]-self.pos[0])/(self.animtime-self.progress),
                        self.pos[1] + (self.queue[0][1]-self.pos[1])/(self.animtime-self.progress))
            self.progress += 1

    def render(self, screen: pygame.Surface, level) -> None:
        """
        renders self onto a screen
        :param screen: pygame surface to blit image on
        """
        self.rect.center = Tower.calc_center((self.pos[1] - level, self.pos[0]))
        screen.blit(self.frames[self.frame_number], self.rect)


if __name__ == '__main__':
    print("this module is for describing the functions and classes of the game 'Higher', it's not supposed to be "
          "launched directly. To learn more about the game, visit https://github.com/kligunov-id/higher")
