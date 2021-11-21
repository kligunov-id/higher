from abc import ABC, abstractmethod
from os import path
import pygame

from locals import *
from button import Button

class GameState(ABC):
    """ Abstract class responsible for controlling all game elements:
        * User input handling
        * Model and animation states update
        * Screen rendering
    """
    def __init__(self):
        pass

    @abstractmethod
    def render(self) -> pygame.Surface:
        """ Composes all visible objects
        :returns: pygame.Surface with the result
        """
        pass

    @abstractmethod
    def handle(self, event: pygame.event.Event) -> None:
        """ Handles all user input events
        :param event: pygame.event.Event to be handled
        """
        pass

    @abstractmethod
    def update(self) -> None:
        """ Calculates new model and animation states """
        pass

class Game:
    """ Wrapper class which resposibility is to allow state switching """
    def __init__(self):
        """ Initializes the only memeber """
        self.switch_to(MainMenu())

    def switch_to(self, new_state: GameState):
        """ Changes game state
        :param new_state: New state, must be an instance of a class derivated from GameState 
        """
        self.state = new_state
        self.state.game = self
        
        # Passes over function calls to state object
        self.render = self.state.render
        self.handle = self.state.handle
        self.update = self.state.update

class MainMenu(GameState):
    """ Represents the starting menu """
    
    def __init__(self):
        """ Initializes menu with buttons """
        def start_game():
             self.game.switch_to(MainMenu())

        self.start_button = Button(TEXT_START, (WIDTH / 2, 0.4 * HEIGHT), action=start_game)
        self.quit_button = Button(TEXT_QUIT, (WIDTH / 2, 0.6 * HEIGHT), action=exit)
        self.buttons = [self.start_button, self.quit_button]
        
        self.font = pygame.font.Font(path.join('resources', 'fonts', FONT_NAME), FONT_SIZE)

    def render(self) -> pygame.Surface:
        """ Renders title and menu buttons
        :returns: PyGame surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        text_surface = self.font.render(TITLE, True, Color.WHITE)
        text_rect = text_surface.get_rect(center = (WIDTH / 2, 0.1 * HEIGHT))
        screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.render(screen)
        
        return screen

    def update(self) -> None:
        """ Animates buttons """
        for button in self.buttons:
            button.update()

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles mouse clicks
        :param event: PyGame event to be handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.handle(event)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game()
    clock = pygame.time.Clock()
    finished = False

    # Main cycle
    while not finished:
        clock.tick(FPS)
        # Handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            else:
                game.handle(event)

        game.update()

        # Renders game
        screen.blit(game.render(), (0, 0))

        # Updates screen
        pygame.display.update()
        screen.fill(Color.BLACK)
    pygame.quit()

if __name__ == '__main__':
    main()
