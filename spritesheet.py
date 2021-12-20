import pygame
from os import path
from locals import WIDTH, HEIGHT

""" 
Implements SpriteSheet

Classes:

    SpriteSheet
"""

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))


class SpriteSheet:
    
    """ Is responsible for loading spritesheets from files and extraction of individual sprites"""

    def __init__(self, filename: str):
        """ Loads the sheet from given file 
        :param filename: Name of the .png sprite sheet """
        try:
            self.sheet = pygame.image.load(path.join('resources', 'images', filename)).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle: pygame.Rect, colorkey=None) -> pygame.Surface:
        """
        Load a specific image from a specific rectangle.
        :param rectangle: (x, y, width, height) of the specified image part, or a pygame.Rect object
        :param colorkey: the colorkey of the image
        :return: pygame.Surface containing the requested image
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self,
                  rects: list[pygame.Rect] | list[tuple[int, int, int, int]],
                  colorkey=None) -> list[pygame.Surface]:
        """
        Load a whole bunch of images and return them as a list.
        :param rects: rectangles (x, y, width, height) to extract the images at
        :param colorkey: colorkey of the images
        :return:  list of the extracted images
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self,
                   rect: pygame.Rect | tuple[int, int, int, int],
                   image_count: int,
                   colorkey=None) -> list[pygame.Surface]:
        """
        Load a whole strip of images, and return them as a list.
        :param rect: pygame.Rect or (x, y, width, height) - the rectangle of the left-most image
        :param image_count: the amount of images
        :param colorkey: colorkey of the images
        :return:  list of the extracted images
        """
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
