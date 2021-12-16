from os import path

"""
Defines global scope constants

Classes:
    
    Color
    TEXT
    MUSIC

Constants:

    FPS
    WIDTH, HEIGHT

    FONT_NAME, FONT_SIZE
    
    TITLE

Function:

    next_track() -> None

"""


class Color:
    """ Defines a set of colors used in the project """

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DEEP_BLUE = (0, 17, 102)
    CITRINE = (204, 204, 0)


# Refresh rate
FPS = 30

# Screen resolution
WIDTH, HEIGHT = 1280, 720

# Font
FONT_NAME = "SUPERSCR.TTF"
FONT_SIZE = 50
FONT_PATH = path.join('resources', 'fonts', FONT_NAME)

# In-game text
TITLE = "Higher"

class TEXT:
    """ Stores game text messages as static variables """
    START = "New Game"
    QUIT = "Quit"
    BACK_MENU = "Back to Menu"
    RESTART = "Play Again"
    GAME_OVER = "Game over!"
    SCORE = "Your Score:"
    SELECT_TRACK_INVITATION = "Choose your soundtrack:"
    SELECT_TRACK = "Select Track"
    DIFFICULTY = ""

class MUSIC:
    TITLES = ["Absolute Valentine - In the 42nd Street", "Opening Animal Crossing"]
    DIFFICULTIES = ["Hard", "BROKEN_BEAT"]
    I = -1
    
    TITLE = None
    PATH = None
    BEAT_PATH = None
    
    PLAY_ERROR = "!!! Failed to play music !!!"
    
    @staticmethod
    def next_title() -> None:
        """ Cyclically changes soundtrack """
        MUSIC.I = (MUSIC.I + 1) % len(MUSIC.TITLES)
        MUSIC.TITLE = MUSIC.TITLES[MUSIC.I]
        MUSIC.PATH = path.join("resources", "music", MUSIC.TITLE + ".mp3")
        MUSIC.BEAT_PATH = path.join("resources", "beatlines", MUSIC.TITLE + ".txt")
        TEXT.DIFFICULTY = f"(Difficulty: {MUSIC.DIFFICULTIES[MUSIC.I]})"

MUSIC.next_title()