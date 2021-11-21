"""
Defines global scope constants

Classes:
    
    Color

Functions:

Constants:

    FPS
    WIDTH, HEIGHT
    FONT_NAME, FONT_SIZE

"""

class Color:
    """ Defines a set of colors used in the project """

    RED  = (255, 0, 0)
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