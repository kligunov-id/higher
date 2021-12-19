from abc import ABC, abstractmethod
from button import ButtonList, Button
from model import Player, Tower
import beatline
from abilities import *
from locals import TEXT, MUSIC

class Settings:
    """ Singleton class responsible for transferring of settings between different GameStates """
    _instance = None

    def __init__(self):
        Settings._instance = self
        self.ability_bar = AbilityBar(None)

    @staticmethod
    def get_instance():
        """ :return: the only instance of Game """
        if Settings._instance is None:
            Settings()
        return Settings._instance

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
        
        self.button_list = ButtonList((WIDTH / 2, 0.32 * HEIGHT), 0.18 * HEIGHT)
        # Start button
        self.button_list.construct_button(TEXT.START,
            action=lambda: Game.switch_to(GameSession()))
        # Track selection button
        self.button_list.construct_button(TEXT.SELECT_TRACK,
            action=lambda: Game.switch_to(MusicSelectionMenu()))
        # Ability selection button
        self.button_list.construct_button(TEXT.SELECT_ABILITY,
            action=lambda: Game.switch_to(AbilitySelectionMenu()))
        # Quit button
        self.button_list.construct_button(TEXT.QUIT,
            action=exit,
            keys=[pygame.K_ESCAPE, pygame.K_BACKSPACE])

        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def render(self) -> pygame.Surface:
        """ Renders title and menu buttons
        :returns: PyGame surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        text_surface = self.font.render(TITLE, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 0.1 * HEIGHT))
        screen.blit(text_surface, text_rect)

        self.button_list.render(screen)
        
        return screen

    def update(self) -> None:
        """ Animates buttons """
        self.button_list.update()

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles mouse clicks
        :param event: PyGame event to be handled
        """
        self.button_list.handle(event)


class GameOver(GameState):
    """ Represents the game over screen """

    def __init__(self, score=0):
        """ Initializes menu with buttons and score"""
        super().__init__()

        self.button_list = ButtonList((WIDTH / 2, 0.6 * HEIGHT), 0.2 * HEIGHT)
        # Restart button
        self.button_list.construct_button(TEXT.RESTART,
            action=lambda: Game.switch_to(GameSession()))
        # Back button
        self.button_list.construct_button(TEXT.BACK_MENU,
            action=lambda: Game.switch_to(MainMenu()),
            keys=[pygame.K_ESCAPE, pygame.K_BACKSPACE])
        
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.score = score

    def render(self) -> pygame.Surface:
        """ Renders game over message and menu buttons
        :returns: PyGame surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        score_surface = self.font.render(TEXT.SCORE + str(self.score), True, Color.WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH/2, 0.2 * HEIGHT))
        text_surface = self.font.render(TEXT.GAME_OVER, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 0.1 * HEIGHT))
        screen.blit(text_surface, text_rect)
        screen.blit(score_surface, score_rect)

        self.button_list.render(screen)
        
        return screen

    def update(self) -> None:
        """ Animates buttons """
        self.button_list.update()

    def handle(self, event: pygame.event.Event) -> None:
        """ Handles mouse and keyboard input
        :param event: PyGame event to be handled
        """
        self.button_list.handle(event)


class GameSession(GameState):
    """represents the gameplay screen"""

    def __init__(self):
        """initialises playing field, player model, abilities, and beatline. Also starts music"""
        super().__init__()

        self.score = 0
        self.tower = Tower()
        self.beatline = beatline.DrawableLine((WIDTH / 2, HEIGHT * 0.8), WIDTH / 2, MUSIC.BEAT_PATH, 2000)
        self.ability_bar = AbilityBar(self.tower.move_sequence)
        self.ability_bar.copy_abilities(Settings.get_instance().ability_bar)
        self.dynamic_elements = [self.beatline, self.ability_bar, self.tower]

        try:
            pygame.mixer.music.load(MUSIC.PATH)
            pygame.mixer.music.play()
        except pygame.error:
            print(MUSIC.PLAY_ERROR)

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
        if not self.tower.is_player_alive():
            pygame.mixer.music.stop()
            Game.switch_to(GameOver(self.score))
        for elem in self.dynamic_elements:
            elem.update()
        if self.beatline.cleanup():
            self.tower.move_floor(1)

class MusicSelectionMenu(GameState):
    """ Represents music selection screen accessible from main menu """

    def __init__(self):
        """ Initializes buttons and font """
        self.button_list = ButtonList((WIDTH / 2, 0.4 * HEIGHT), 0.4 * HEIGHT)
        
        def next():
            MUSIC.next_title()
            self.button_list.buttons[0].update_text(MUSIC.TITLE)

        self.button_list.construct_scroll(MUSIC.TITLES,
            post_action=lambda i:MUSIC.set_title(i))
        self.button_list.construct_button(TEXT.BACK_MENU,
            action=lambda: Game.switch_to(MainMenu()),
            keys=[pygame.K_ESCAPE, pygame.K_BACKSPACE])

        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def render(self) -> pygame.Surface:
        """ Renders buttons and text """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        text_surface = self.font.render(TEXT.SELECT_TRACK_INVITATION, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 0.1 * HEIGHT))
        screen.blit(text_surface, text_rect)
        text_surface = self.font.render(TEXT.DIFFICULTY, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 0.6 * HEIGHT))
        screen.blit(text_surface, text_rect)
        
        self.button_list.render(screen)

        return screen
    
    def handle(self, event: pygame.event.Event) -> None:
        """ Handles mouse and keyboard input
        :param event: PyGame event to be handled
        """
        self.button_list.handle(event)

    def update(self) -> None:
        """ Animates buttons """
        self.button_list.update()

class AbilitySelectionMenu(GameState):
    """ Represents ability selection screen accessible from main menu """

    def __init__(self):
        """ Initializes buttons and font """
        self.button_list = ButtonList((WIDTH * 0.6, 0.27 * HEIGHT), 0.15 * HEIGHT)
        self.ability_bar = Settings.get_instance().ability_bar
        def set_into_slot(k):
            return lambda i: self.ability_bar.set_ability(k, ability_list[i]())
        for k in range(4):
            self.button_list.construct_scroll(ability_names,
                post_action=set_into_slot(k),
                starting_i=ability_names.index(self.ability_bar.abilities[k].name))

        self.button_list.add_button(Button(TEXT.BACK_MENU,
            (WIDTH * 0.6, 0.9 * HEIGHT),
            action=lambda: Game.switch_to(MainMenu()),
            keys=[pygame.K_ESCAPE, pygame.K_BACKSPACE]))

        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def render(self) -> pygame.Surface:
        """ Renders buttons and text """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        text_surface = self.font.render(TEXT.SELECT_ABILITY_INVITATION, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH * 0.6, 0.1 * HEIGHT))
        screen.blit(text_surface, text_rect)
        
        self.button_list.render(screen)
        self.ability_bar.render(screen)

        return screen
    
    def handle(self, event: pygame.event.Event) -> None:
        """ Handles mouse and keyboard input
        :param event: PyGame event to be handled
        """
        self.button_list.handle(event)

    def update(self) -> None:
        """ Animates buttons """
        self.button_list.update()


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
