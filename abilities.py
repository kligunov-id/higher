import os.path
from os import path
from enum import Enum, auto
import pygame
from abc import ABC
from spritesheet import *
from locals import *
from model import *


def weirdscale(surface, size):
    return pygame.transform.scale(pygame.transform.scale2x(pygame.transform.scale2x(surface)), size)


class Ability(ABC):
    """ Renders ability, tracks it CD and executes it """

    def __init__(self, abilitybar, cd: int = 5):
        """ Initilizes CD timer, binds ability with the abilitybar
        :param abilitybar: abilitybar to bind the ability with
        :param cd: cooldown of the ability
        """
        self.abilitybar = abilitybar
        self.cd_left = 0
        self.player = self.abilitybar.player
        self.spritesheet = self.abilitybar.spritesheet
        self.KEY = None
        self.CD = cd

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
        """ Recharges CD and executes ability if ready
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
    keys = [pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l]
    height = int(HEIGHT * 0.8)
    width = int(height * 0.25)
    x, y = int(WIDTH / 5), int(height / 2)

    def __init__(self, spritesheet, player: Player, pos: tuple[int, int] = None):
        """
        initiates AbilityBar with void abilities
        hardcoded to have exactly 4
        """
        self.player = player
        self.spritesheet = spritesheet
        if pos:
            self.x, self.y = pos
            self.height = self.y * 2
            self.width = int(self.height / 4)
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
        return int(self.width / 2), int(self.height / 8 + self.height / 4 * place)

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

    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 960

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move_sequence((-1, 0), (-1, 0), (0, 1))

    def render(self) -> pygame.Surface:
        """:return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class KnightUpLeft(Ability):
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 640

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    """ Represents top-left dash activated by L key """

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move_sequence((0, 1), (0, 1), (-1, 0))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability text rendered on it """
        return self.frames[self.cd_left]


class KnightUpRight(Ability):
    """ Represents top-right dash activated by L key """
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 320

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move_sequence((0, 1), (0, 1), (1, 0))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class KnightRightUp(Ability):
    """ Represents left-top dash activated by semicolon """
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 0

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.player.move_sequence((1, 0), (1, 0), (0, 1))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class RushUp(Ability):
    """Represents three-steps-up dash"""
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 1280

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    def execute(self) -> None:
        """"""
        self.player.move_sequence((0, 1), (0, 1), (0, 1))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class Hop(Ability):
    """Represents a teleport two tiles up"""
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 1600

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    def execute(self) -> None:
        """"""
        self.player.move_sequence((0, 2))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class Mirror(Ability):
    """Mirrors the player's X position"""
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 1600

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)
        for i, frame in enumerate(self.frames):
            self.frames[i] = pygame.transform.scale(frame, (self.abilitybar.width, self.abilitybar.width))

    def execute(self) -> None:
        """executes the ability effect"""
        newx = self.player.tower.WIDTH - self.player.x - 1
        self.player.move_sequence((newx - self.player.x, 0))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]
