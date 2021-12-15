from abc import ABC, abstractmethod
from button import Button
import model
import beatline
from abilities import *


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
    """ Singleton wrapper class which resposibility is to allow state switching """
    state: GameState
    _instance = None

    def __init__(self):
        """ Initializes the only memeber """
        Game._instance = self
        self.switch_to(MainMenu())

    def _switch_to(self, new_state: GameState) -> None:
        """ Changes game state
        :param new_state: New state, *instance* of a derivative from GameState
        .. note: For internal use only
        """
        self.state = new_state
        
        # Passes over function calls to GameState object
        self.render = self.state.render
        self.handle = self.state.handle
        self.update = self.state.update

    @staticmethod
    def switch_to(new_state: GameState) -> None:
        """ Changes game state
        :param new_state: New state, *instance* of a derivative from GameState 
        """
        Game._switch_to(Game._instance, new_state)


class MainMenu(GameState):
    """ Represents the starting menu """
    
    def __init__(self):
        """ Initializes menu with buttons """
        super().__init__()

        self.start_button = Button(TEXT_START, (WIDTH / 2, 0.4 * HEIGHT),
            action=lambda :Game.switch_to(GameSession()))
        self.quit_button = Button(TEXT_QUIT, (WIDTH / 2, 0.6 * HEIGHT), action=exit)
        self.buttons = [self.start_button, self.quit_button]
        
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def render(self) -> pygame.Surface:
        """ Renders title and menu buttons
        :returns: PyGame surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        text_surface = self.font.render(TITLE, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 0.1 * HEIGHT))
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


class GameOver(GameState):
    """ Represents the game over screen """

    def __init__(self, score=0):
        """ Initializes menu with buttons and score"""
        super().__init__()

        self.restart_button = Button(TEXT_RESTART, (WIDTH / 2, 0.6 * HEIGHT),
            action=lambda: Game.switch_to(GameSession()))
        self.menu_button = Button(TEXT_BACK_MENU, (WIDTH / 2, 0.8 * HEIGHT),
            action=lambda: Game.switch_to(MainMenu()))
        self.buttons = [self.restart_button, self.menu_button]
        
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        self.score = score

    def render(self) -> pygame.Surface:
        """ Renders game over message and menu buttons
        :returns: PyGame surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        score_surface = self.font.render(TEXT_SCORE + str(self.score), True, Color.WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH/2, 0.2 * HEIGHT))
        text_surface = self.font.render(TEXT_GAME_OVER, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 0.1 * HEIGHT))
        screen.blit(text_surface, text_rect)
        screen.blit(score_surface, score_rect)

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


class GameSession(GameState):
    """represents the gameplay screen"""

    def __init__(self):
        """initialises playing field, player model, abilities, and beatline. Also starts music"""
        super().__init__()

        self.score = 0

        self.abilitysheet = SpriteSheet('abilitysheet.png')

        self.tower = model.Tower()
        self.beatline = beatline.DrawableLine((WIDTH/2, HEIGHT * 0.8), WIDTH/2, MUSIC_BEAT_PATH, 2000)
        self.abilitybar = AbilityBar(self.abilitysheet, self.tower.player)

        self.abilitybar.set_ability(0, KnightLeftUp(self.abilitybar))
        self.abilitybar.set_ability(1, KnightUpLeft(self.abilitybar))
        self.abilitybar.set_ability(2, KnightUpRight(self.abilitybar))
        self.abilitybar.set_ability(3, KnightRightUp(self.abilitybar))

        self.dynamic_elements = [self.beatline, self.abilitybar, self.tower]

        try:
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.play()
        except pygame.error:
            print(MUSCI_PLAY_ERROR)

    def handle(self, event):
        """handles user input, checks whether any beats are active"""
        if event.type == pygame.KEYDOWN:
            if self.beatline.is_active():
                self.beatline.deactivate()
                for elem in self.dynamic_elements:
                    elem.handle(event)
                self.score += 1

    def render(self) -> pygame.Surface:
        """renders the tower, player model and beatline onto the screen"""
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for elem in self.dynamic_elements:
            elem.render(screen)
        return screen

    def update(self):
        """switches to the game over screen if the player is dead"""
        if not self.tower.player.is_alive():
            pygame.mixer.music.stop()
            Game.switch_to(GameOver(self.score))
        for elem in self.dynamic_elements:
            elem.update()
        if self.beatline.cleanup():
            self.tower.move_floor(1)


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
