import os.path
from os import path
from enum import Enum, auto
import pygame
from abc import ABC

from locals import *
from model import *

class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(os.path.join('resources', 'images', filename)).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

def weirdscale(surface, size):
    return pygame.transform.scale(pygame.transform.scale2x(pygame.transform.scale2x(surface)), size)

class Ability(ABC):
    """ Renders ability, tracks it CD and executes it """

    def __init__(self, abilitybar, CD: int = 5):
        """ Initilizes CD timer, binds ability with the player """
        self.abilitybar = abilitybar
        self.cd_left = 0
        self.player = self.abilitybar.player
        self.spritesheet = self.abilitybar.spritesheet
        self.KEY = None
        self.CD = CD

    def render(self) -> pygame.Surface:
        """
        renders the ability.
        :return: surface with the ability text rendered on it
        """
        pass

    def update(self) -> None:
        """ For now abilities have now animation or progression """
        pass

    def handle(self, event: pygame.event.Event) -> None:
        """ Recharges CD and executes ability
        :param event: Event to be handled"""
        if self.is_active() and self.KEY and event.key == self.KEY:
            self.execute()
            self.cd_left = self.CD
        self.cd_left -= 1
        self.cd_left = max(self.cd_left, 0)

    def is_active(self) -> bool:
        """ :returns: True if cd is over """
        return self.cd_left <= 0

    def execute(self) -> None:
        """ Executes the ability """
        pass

class AbilityBar:
    keys = [pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON]
    height = int(HEIGHT * 0.8)
    width = int(height * 0.25)
    x, y = int(width/2), int(height/2)

    def __init__(self, player: Player, pos: tuple[int, int] = None):
        """
        initiates AbilityBar with void abilities
        hardcoded to have exactly 4
        """
        self.player = player
        if pos:
            self.x, self.y = pos
            height = self.y * 2
            width = int(height / 4)
        self.abilities = [Ability(self), Ability(self), Ability(self), Ability(self)]

    def update(self):
        for ability in self.abilities:
            ability.update()

    def render(self, screen):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for place, ability in enumerate(self.abilities):
            aimage = ability.render()
            arect = aimage.get_rect(center=self.get_pos(place))
            surf.blit(aimage, arect)
        screen.blit(surf, surf.get_rect(center=(self.x, self.y)))

    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return
        for ability in self.abilities:
            ability.handle(event)

    def get_pos(self, place: int) -> tuple[int, int]:
        """
        calculates the center of the ability image from it's place on the ability bar
        :param place: place of the ability on the abilitybar - from 0 to 3
        :return: pos (x, y) of the center of the ability image
        """
        return (int(self.width / 2), int(self.height / 8 + self.height / 4 * place))

    def set_ability(self, place: int, ability: Ability) -> None:
        """
        sets an ability onto itself
        :param place: the place of the ability on the ability bar, value between 0 and 3
        :param ability: the ability, created, but not constructed
        :return: None
        """
        ability.KEY = self.keys[place]
        self.abilities[place] = ability


class KnightLeftUp(Ability):
    """ Represents left-top dash activated by J key """

    def __init__(self, *args):
        """ Initilizes the ability, without constructing it fully."""
        super().__init__(*args)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move(-1, 0)
        self.player.move(-1, 0)
        self.player.move(0, 1)

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability text rendered on it """
        font = pygame.font.Font(path.join('resources', 'fonts', FONT_NAME), FONT_SIZE - 20)
        self.text_surface = font.render(f"DashJ CD: {self.cd_left}", True, Color.WHITE)
        return self.text_surface

class KnightUpLeft(Ability):
    def __init__(self, *args):
        """ Initilizes the ability, without constructing it fully."""
        super().__init__(*args)

    """ Represents top-left dash activated by L key """

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move(0, 1)
        self.player.move(0, 1)
        self.player.move(-1, 0)

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability text rendered on it """
        font = pygame.font.Font(path.join('resources', 'fonts', FONT_NAME), FONT_SIZE - 20)
        self.text_surface = font.render(f"DashK CD: {self.cd_left}", True, Color.WHITE)
        return self.text_surface

class KnightUpRight(Ability):
    """ Represents top-right dash activated by L key """

    def __init__(self, *args):
        """ Initilizes the ability, without constructing it fully."""
        super().__init__(*args)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move(0, 1)
        self.player.move(0, 1)
        self.player.move(1, 0)

    def render(self) -> pygame.Surface:
        """ Displays current CD
        text_surface = font.render(f"DashJ CD: {self.cd_left}", True, Color.WHITE) """
        font = pygame.font.Font(path.join('resources', 'fonts', FONT_NAME), FONT_SIZE - 20)
        self.text_surface = font.render(f"DashL CD: {self.cd_left}", True, Color.WHITE)
        return self.text_surface

class KnightRightUp(Ability):
    """ Represents left-top dash activated by semicolon """

    def __init__(self, *args):
        """ Initilizes the ability, without constructing it fully."""
        super().__init__(*args)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move(1, 0)
        self.player.move(1, 0)
        self.player.move(0, 1)

    def render(self) -> pygame.Surface:
        """ Displays current CD
        text_surface = font.render(f"DashJ CD: {self.cd_left}", True, Color.WHITE) """
        font = pygame.font.Font(path.join('resources', 'fonts', FONT_NAME), FONT_SIZE - 20)
        self.text_surface = font.render(f"DashS CD: {self.cd_left}", True, Color.WHITE)
        return self.text_surface