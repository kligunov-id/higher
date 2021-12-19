from model import *
from abc import ABC
from spritesheet import SpriteSheet

"""
    Stores and renders abilities via AbilityBar
    Implements different abilities

    Classes:

        Ability
        AbilityBar

        KnightLeftUp, KnightUpLeft, KnightUpRight, KnightRightUp
        RushUp, Hop, Mirror

    Constants:

        ability_names
        ability_list
"""

class Ability(ABC):
    """ Renders ability, tracks it CD and executes it """
    
    name = "Void Ability"

    def __init__(self, move_sequence=None, cd: int = 5):
        """ Initilizes CD timer, binds ability with the abilitybar
        :param spritesheet: Spritesheet with all abilities
        :param move_sequence: Move function(moves:list[tuple[int, int]]) -> None 
        :param cd: cooldown of the ability
        """
        self.cd_left = 0
        self.spritesheet = SpriteSheet('abilitysheet.png')
        self.move_sequence = move_sequence
        self.key = None
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
        if self.is_active() and self.key and event.key == self.key:
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
    """ Stores and manages abilities, renders and executes them """

    keys = [pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l]
    height = int(HEIGHT * 0.8)
    width = int(height * 0.25)
    x, y = int(WIDTH / 5), int(height / 2)

    def __init__(self, move_sequence, pos: tuple[int, int] = None):
        """ Initializes AbilityBar wiht 4 default abilities and binds move function
        :param move_sequence: Move function(moves:list[tuple[int, int]]) -> None
        :param pos: ??????????
        """
        self.move_sequence = move_sequence
        if pos:
            self.x, self.y = pos
            self.height = self.y * 2
            self.width = int(self.height / 4)
        self.abilities = [None] * 4
        self.set_default_abilities()

    def set_default_abilities(self) -> None:
        """ Fills slots with Knight abilities """
        self.set_ability(0, KnightLeftUp())
        self.set_ability(1, KnightUpLeft())
        self.set_ability(2, KnightUpRight())
        self.set_ability(3, KnightRightUp())

    def copy_abilities(self, ability_bar) -> None:
        """ Fills slots with abilities from another ability bar """
        if ability_bar is None:
            return
        for i, ability in enumerate(ability_bar.abilities):
            self.set_ability(i,
                ability_list[ability_names.index(ability.name)]())

    def update(self) -> None:
        """ Updates animation states of abilities """
        for ability in self.abilities:
            ability.update()

    def render(self, screen: pygame.Surface) -> None:
        """ Renders ability sprite
        :param screen: PyGame surface to blit onto """
        surf = pygame.Surface((self.width, self.height + 50), pygame.SRCALPHA)
        for place, ability in enumerate(self.abilities):
            aimage = ability.render()
            arect = aimage.get_rect(center=self.get_pos(place))
            surf.blit(aimage, arect)
        screen.blit(surf, surf.get_rect(center=(self.x, self.y + 70)))

    def handle(self, event: pygame.event.Event) -> None:
        """ Executes abilities when binded keys are pressed """
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
        return int(self.width / 2), int(self.height / 8 + (self.height / 4 + 10) * place)

    def set_ability(self, slot: int, ability: Ability) -> None:
        """
        Places ability into the slot
        :param slot: the place of the ability on the ability bar, value between 0 and 3
        :param ability: the ability, created, but not constructed
        """
        ability.key = self.keys[slot]
        ability.move_sequence = self.move_sequence
        self.abilities[slot] = ability

        for i, frame in enumerate(ability.frames):
            ability.frames[i] = pygame.transform.scale(frame, (self.width, self.width))


class KnightLeftUp(Ability):
    """ Represents left-top dash """

    name = "Knight Left-Up"
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 960

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.move_sequence((-1, 0), (-1, 0), (0, 1))

    def render(self) -> pygame.Surface:
        """:return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class KnightUpLeft(Ability):
    """ Represents top-left dash """

    name = "Knight Up-Left"
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 640

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.move_sequence((0, 1), (0, 1), (-1, 0))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability text rendered on it """
        return self.frames[self.cd_left]


class KnightUpRight(Ability):
    """ Represents top-right dash """

    name = "Knight Up-Right"
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 320

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.move_sequence((0, 1), (0, 1), (1, 0))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class KnightRightUp(Ability):
    """ Represents left-top dash """

    name = "Knight Right-Up"
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 0

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)

    def execute(self) -> None:
        """ Teleports to the left and top """
        self.move_sequence((1, 0), (1, 0), (0, 1))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class RushUp(Ability):
    """ Represents three-steps-up dash """

    name = "Rush Up"
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 1280

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)

    def execute(self) -> None:
        """"""
        self.move_sequence((0, 1), (0, 1), (0, 1))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]


class Hop(Ability):
    """ Represents a teleport two tiles up """

    name = "Hop"
    # coordinates of the upper-left corner of the first frame of animation on the spritesheet
    cordsx = 0
    cordsy = 1600

    def __init__(self, *args):
        """ Initilizes the ability"""
        super().__init__(*args)
        self.frames = self.spritesheet.load_strip((self.cordsx, self.cordsy, 320, 320), 6, Color.WHITE)

    def execute(self) -> None:
        """"""
        self.move_sequence((0, 2))

    def render(self) -> pygame.Surface:
        """ Displays current CD
        :return: surface with the ability image rendered on it """
        return self.frames[self.cd_left]

'''
class Mirror(Ability):
    """ Mirrors the player's X position """
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
'''

ability_list = [KnightLeftUp, KnightUpLeft, KnightUpRight, KnightRightUp, RushUp, Hop]
ability_names = [ability.name for ability in ability_list]

if __name__ == '__main__':
    print("this module is for describing the abilities of the game 'Higher', it's not supposed to be "
          "launched directly. To learn more about the game, visit https://github.com/kligunov-id/higher")
