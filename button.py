import pygame
import os.path


class Button():

    def __init__(self, image, rect, text, fontname, fontsize, color):
        # хитбокс
        self.rect = rect
        #картинка
        self.image = image
        self.image_rect = self.image.get_rect(center=self.rect.center)
        #текст
        self.fontname = fontname
        self.fontsize = fontsize
        self.color = color
        self.update_text(text)

    def update_text(self, text=''):
        if text:
            self.text = text
        self.font = pygame.font.Font(os.path.join('resources', 'fonts', self.fontname), int(self.fontsize))
        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        '''draws self onto a surface'''
        screen.blit(self.image, self.image_rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_mouse_on(self, pos):
        """
        Checks if mouse is hovering over the button
        :param pos: Mouse position (x, y)
        """
        return self.rect.collidepoint(pos)


class ButtonFactory:

    def __init__(self, fontname, fontsize, color):
        self.fontname = fontname
        self.fontsize = fontsize
        self.color = color

    def newbutton(self, imagename:str, pos, size, text:str):
        image = pygame.image.load(os.path.join('resources', 'images', imagename)).convert()
        rect = pygame.rect.Rect(pos, size)
        rect.center = pos
        button = Button(image, rect, text, self.fontname, self.fontsize, self.color)
        return button