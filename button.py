import pygame
from pygame.rect import Rect

from locals import FONT_PATH, Color
from os import path

""" 
Implements buttons and keyboard nevigation through menues

Classes:

    Button
    ButtonList
"""

class Button:
    text: str
    font: pygame.font.Font
    text_surface: pygame.Surface
    text_rect: Rect

    FONTSIZE_SMALL = 60
    FONTSIZE_BIG = 70
    ANIMATION_SPEED = 0.8
    FONT_PATH = FONT_PATH
    COLOR = Color.WHITE

    def __init__(self, text: str, center: tuple[int, int], action=None, keys=None):
        """ Initializes new button
        :param text: Displayed button text
        :param center: List of coordinates (x, y) of the button text
        :param action: Function with 0 parameters which will be called on-click
        :param keys: Pygame key id to trigger button
        """
        self.center = center
        self.fontsize = Button.FONTSIZE_SMALL
        self.action = action
        self.update_text(text)
        self.keys = keys

    def render(self, screen: pygame.Surface) -> None:
        """ Blits button image onto given surface
        :param screen: pygame.Surface to render button on
        """
        screen.blit(self.text_surface, self.text_rect)

    def update_text(self, text="") -> None:
        """ Redraws button with new fontsize and (optionaly) text
        :param text: New text
        """
        if text:
            self.text = text
        self.font = pygame.font.Font(FONT_PATH, int(self.fontsize))
        self.text_surface = self.font.render(self.text, True, Button.COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.center)

    def update(self) -> None:
        """ Animates button """
        if self.is_mouse_on():
            self.fontsize += Button.ANIMATION_SPEED
        else:
            self.fontsize -= Button.ANIMATION_SPEED
        # This checks that fontsize in inside [FONTSIZE_SMALL, FONTSIZE_BIG]
        self.fontsize = max(Button.FONTSIZE_SMALL, self.fontsize)
        self.fontsize = min(Button.FONTSIZE_BIG, self.fontsize)
        # This redraws button image and recalculates rect
        self.update_text()

    def is_mouse_on(self) -> bool:
        """ Checks if mouse is hovering over the button
        :returns : True if mouse is hovering over the button
        """
        return self.text_rect.collidepoint(pygame.mouse.get_pos())
    
    def handle(self, event: pygame.event.Event) -> None:
        """ Handles mouse clicks and key presses
        :param event: PyGame event to be handled
        """
        should_trigger = ((event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_on())
                       or (event.type == pygame.KEYDOWN and self.keys and event.key in self.keys))

        if should_trigger and self.action is not None:
            self.action()

class ButtonList:
    """ Stores a set of buttons, implements navigation. """


    def __init__(self, topmid: tuple[int, int], h_step: int):
        """ Initializes empty button list and sets layout
        :param topmid: Coordinates (width, height) of the first button
        :param h_step: Difference between heights of adjacent buttons """
        self.buttons = []
        self.i = 0
        self.topmid = topmid
        self.h_step = h_step
    
    def add_button(self, button:Button) -> None:
        """ Add already existing button
        :param button: Button instance to add to list
        ..note:: It is preferable to use construct_button()"""
        self.buttons.append(button) 
    
    def construct_button(self, text: str, action=None, keys=None) -> None:
        """ Creates new button in place
        :param text: Displayed button text
        :param action: Function with 0 parameters which will be called on-click
        :param keys: Pygame key ids to trigger button
        """
        width, height = self.buttons[-1].center if self.buttons else self.topmid
        height += self.h_step if self.buttons else 0
        self.buttons.append(Button(text, (width, height), action, keys))

    def render(self, screen: pygame.Surface) -> None:
        """ Renders buttons and the pointer
        :param screen: pygame.Surface to blit on
        """
        for button in self.buttons:
            button.render(screen)
        # Renders pointer (">") to the active button
        active_button = self.buttons[self.i]
        text_surface = active_button.font.render("> ", True, Button.COLOR)
        text_rect = text_surface.get_rect(topright=active_button.text_rect.topleft)
        screen.blit(text_surface, text_rect)

    def update(self) -> None:
        """ Animates buttons """
        for button in self.buttons:
            button.update()


    def handle(self, event: pygame.event.Event) -> None:
        """ Handles button navigation and activation through clicks or keystrokes
        :param event: PyGame event to be handled
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.i = (self.i - 1) % len(self.buttons)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.i = (self.i + 1) % len(self.buttons)
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.buttons[self.i].action()
        for button in self.buttons:
            button.handle(event)

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((600, 600))

    buttons = ButtonList((300, 300), 100)
    buttons.construct_button("Quit", action=exit)
    buttons.construct_button("Quit2", action=exit)
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
                buttons.handle(event)

        buttons.update()
        buttons.render(screen)

        # Updates screen
        pygame.display.update()
        screen.fill(Color.BLACK)
    pygame.quit()
