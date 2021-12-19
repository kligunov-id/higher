import pygame
from pygame.rect import Rect

from locals import FONT_PATH, Color

""" 
Implements buttons and keyboard nevigation through menues

Classes:

    Button, Scroll
    ButtonList

Functions:

   trim(text, max_len=20) -> str

"""

def trim(text:str, max_len:int = 30) -> str:
    """ Trims text"""
    if len(text) > max_len:
        text = text[:max_len-3] + "..."
    return text

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
        :param keys: List of Pygame key id-s to trigger button
        """
        self.center = center
        self.fontsize = Button.FONTSIZE_SMALL
        self.action = action
        self.update_text(text)
        self.keys = keys
        self.active = False
    
    def set_active(self, active:bool = True) -> None:
        """ Activates or deactivates button
        :param active: True if button should be activated """
        self.active = active

    def render(self, screen: pygame.Surface) -> None:
        """ Blits button image onto given surface
        :param screen: pygame.Surface to render button on
        """
        screen.blit(self.text_surface, self.text_rect)
        if self.active:
            # Renders pointer (">") to the active button
            text_surface = self.font.render("> ", True, Button.COLOR)
            text_rect = text_surface.get_rect(topright=self.text_rect.topleft)
            screen.blit(text_surface, text_rect)

    def update_text(self, text="") -> None:
        """ Redraws button with new fontsize and (optionaly) text
        :param text: New text
        """
        if text:
            self.text = text
        self.font = pygame.font.Font(FONT_PATH, int(self.fontsize))
        self.text_surface = self.font.render(trim(self.text), True, Button.COLOR)
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
                       or (event.type == pygame.KEYDOWN and self.keys and event.key in self.keys)
                       or (event.type == pygame.KEYDOWN and self.active and event.key == pygame.K_RETURN))

        if should_trigger and self.action is not None:
            self.action()

class Scroll:
    """ Provides selection from the number of entries.
        Is compatible with ButtonList """

    font: pygame.font.Font
    text_surface: pygame.Surface
    text_rect: Rect
    left_surface: pygame.Surface
    left_rect: Rect
    right_surface: pygame.Surface
    right_rect: Rect

    FONTSIZE_SMALL = 60
    FONTSIZE_BIG = 64
    FONT_PATH = FONT_PATH
    COLOR = Color.WHITE

    def __init__(self, options: list[str], center: tuple[int, int], post_action=None, starting_i: int = 0):
        """ Initializes new button
        :param options: Displayed button text
        :param center: List of coordinates (x, y) of the button text
        :param post_action: Function with 1 paramater (number of entry chosen)
                                                to call after each entry change
        :param starting_i: Index of starting entry
        """
        self.options = options
        self.center = center
        self.post_action = post_action
        self.i = starting_i
        self.active = False
        self.size_left = Scroll.FONTSIZE_SMALL
        self.size_right = Scroll.FONTSIZE_SMALL
        self.update_surface()

    def update_surface(self) -> None:
        """ Redraws scroll, arrows and recalculates hitbox """
        font = pygame.font.Font(Scroll.FONT_PATH, Scroll.FONTSIZE_SMALL)
        font_left = pygame.font.Font(Scroll.FONT_PATH, self.size_left)
        font_right = pygame.font.Font(Scroll.FONT_PATH, self.size_right)
        # Text
        self.text_surface = font.render(trim(self.options[self.i]), True, Button.COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.center)
        # Arrows
        self.left_surface = font_left.render(" < ", True, Button.COLOR)
        self.left_rect = self.left_surface.get_rect(midright=self.text_rect.midleft)
        self.right_surface = font_right.render(" > ", True, Button.COLOR)
        self.right_rect = self.right_surface.get_rect(midleft=self.text_rect.midright)

    def update(self) -> None:
        """ Animates scroll """
        # Increases fontsize when mouse is hovering
        if self.is_mouse_on_left():
            self.size_left += 1
        else:
            self.size_left -= 1
        if self.is_mouse_on_right():
            self.size_right += 1
        else:
            self.size_right -= 1
        # Makes sure fontsizes are in range [FONTSIZE_SMALL, FONTSIZE_BIG]
        self.size_left = max(Button.FONTSIZE_SMALL, self.size_left)
        self.size_left = min(Button.FONTSIZE_BIG, self.size_left)
        self.size_right = max(Button.FONTSIZE_SMALL, self.size_right)
        self.size_right = min(Button.FONTSIZE_BIG, self.size_right)
        self.update_surface()

    def render(self, screen: pygame.Surface) -> None:
        """ Blits button image onto given surface
        :param screen: pygame.Surface to render button on
        """
        screen.blit(self.text_surface, self.text_rect)
        if self.active or self.is_mouse_on():
            screen.blit(self.left_surface, self.left_rect)
            screen.blit(self.right_surface, self.right_rect)

    def set_active(self, active:bool = True) -> None:
        """ Activates or deactivates scroll
        :param active: True if scroll should be activated """
        self.active = active

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles key AD/LeftRight entry change
        :param event: PyGame event to be handled
        """
        prev_i = self.i

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.i = (self.i - 1) % len(self.options)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.i = (self.i + 1) % len(self.options)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_on_left():
                self.i = (self.i - 1) % len(self.options)
            if self.is_mouse_on_right():
                self.i = (self.i + 1) % len(self.options)

        if prev_i != self.i and self.post_action is not None:
            self.post_action(self.i)

    def is_mouse_on_left(self) -> bool:
        """ :return: True if mouse is hovering over the left arrow """
        return self.left_rect.collidepoint(pygame.mouse.get_pos()) 
    
    def is_mouse_on_right(self) -> bool:
        """ :return: True if mouse is hovering over the right arrow """
        return self.right_rect.collidepoint(pygame.mouse.get_pos())

    def is_mouse_on(self) -> bool:
        """ :return: True if mouse is hovering over the scroll"""
        return (self.text_rect.collidepoint(pygame.mouse.get_pos()) 
            or self.is_mouse_on_left() or self.is_mouse_on_right())

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
        if not self.buttons:
            button.set_active()
        self.buttons.append(button)
    
    def construct_button(self, text: str, action=None, keys=None) -> None:
        """ Creates new button in place
        :param text: Displayed button text
        :param action: Function with 0 parameters which will be called on-click
        :param keys: Pygame key ids to trigger button
        """
        width, height = self.buttons[-1].center if self.buttons else self.topmid
        height += self.h_step if self.buttons else 0
        new_button = Button(text, (width, height), action, keys)
        if not self.buttons:
            new_button.set_active()
        self.buttons.append(new_button)
    
    def construct_scroll(self, options: list[str], post_action=None, starting_i: int = 0):
        """ Creates and appends new scroll
        :param options: Displayed button text
        :param post_action: Function with 1 paramater (number of entry chosen)
                                                to call after each entry change
        :param starting_i: Index of starting entry
        """
        width, height = self.buttons[-1].center if self.buttons else self.topmid
        height += self.h_step if self.buttons else 0
        new_scroll = Scroll(options, (width, height), post_action, starting_i)
        if not self.buttons:
            new_scroll.set_active()
        self.buttons.append(new_scroll)

    def render(self, screen: pygame.Surface) -> None:
        """ Renders buttons and scrolls
        :param screen: pygame.Surface to blit on
        """
        for button in self.buttons:
            button.render(screen)

    def update(self) -> None:
        """ Animates buttons """
        for button in self.buttons:
            button.update()

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles button navigation and activation through clicks or keystrokes
        :param event: PyGame event to be handled
        """
        if event.type == pygame.KEYDOWN:
            prev_i = self.i
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.i = (self.i - 1) % len(self.buttons)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.i = (self.i + 1) % len(self.buttons)
            # Update active button 
            self.buttons[prev_i].set_active(active=False)
            self.buttons[self.i].set_active()
        for button in self.buttons:
            button.handle(event)

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1200, 600))
    
    names = ["AA", "B", "C"]
    buttons = ButtonList((600, 200), 100)
    buttons.construct_button("Quit", action=exit, keys=[pygame.K_q])
    buttons.construct_button("Hi " * 20, action=lambda:print("Hi"))
    def cool_action(i):
        buttons.buttons[1].update_text(names[i])
    buttons.construct_scroll(names, lambda i: buttons.buttons[1].update_text(names[i]))
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
