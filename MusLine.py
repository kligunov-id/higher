import pygame
import os.path


class Line:
    """
    a class that contains the data of the music line
    Handles unpacking new beats from a file, and validating whether any beats are in the active zone or not
    """

    def __init__(self, pos: tuple[int, int], width: int, filename: str, timeloop: int):
        """
        :param pos: the position (x, y) of the center of the line
        :param width: the width of the line
        :param filename: the name of the file that the line will extract beat data from
        :param timeloop: the amount of milliseconds the beats will be visible on the line
        """
        self.birthtime = pygame.time.get_ticks()
        self.time = 0
        self.filepath = os.path.join('resources', 'beatlines', filename)
        self.timeloop = timeloop
        self.pos = pos
        self.width = width

        # extracting beats for the first time interval
        self.beats = []
        self.last_update = -100000
        self.unpack(0, 2 * timeloop)

    def update(self):
        """
        updates self.time,
        unpacks extra beats once in self.timeloop
        kills beats that have finished their lifespan and updates the live ones
        :return: True is an active beat has been deleted for reaching the end of the line, False in not.
        """
        # update time
        self.time = pygame.time.get_ticks() - self.birthtime

        # unpack beats for the next loop
        if self.time - self.last_update >= 0.9 * self.timeloop:
            self.unpack(self.time + self.timeloop, self.time + 2 * self.timeloop)

        # updates the beats
        for beat in self.beats:
            beat.update()

    def cleanup(self) -> bool:
        """cleans up beats that have reached the end of the beatline, returns True if deleted an Unused beat"""
        if self.beats[0].time - self.time <= -int(self.timeloop / 2):
            return self.beats.pop(0).active

    def handle(self, event):
        """a placeholder function for handling events"""
        pass

    def unpack(self, start_time: int, end_time: int):
        """
        unpacks beats from the self.filepath file
        :param start_time: the first millisecond from which the beats will be unpacked
        :param end_time: the last millisecond to which the beats will be unpacked
        :return: None, instead appends Beat objects to self.beats
        """
        with open(self.filepath, 'r') as f:
            dump = f.readlines()
            for time in dump:
                time = int(float(time.strip()) * 1000)
                if time >= max(start_time, self.last_update + 2000):
                    if time >= end_time:
                        break
                    self.beats.append(DrawableBeat(self, int(time), 200))
        self.last_update = self.time

    def is_active(self):
        """
        checks if any beat is active
        :return: bool
        """
        for beat in self.beats:
            if beat.is_active():
                return True
        return False

    def deactivate(self):
        """prevents any active beats from being active in the future"""
        for beat in self.beats:
            if beat.is_active():
                beat.deactivate()


class DrawableLine(Line):
    """a class that adds visual rendering to the line class"""

    def initiate_images(self, size: tuple[int, int], pointer_size: tuple[int, int] = (6, 40)):
        """
        unpacks images from files, resizes them to parameters
        :param size: the size(width, height) of the line
        :param pointer_size: the size(width, height) of the pointer
        :return: None
        """
        self.image = pygame.image.load(os.path.join('resources', 'images', 'BeatLine.png'))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, size)

        self.pointer_image = pygame.image.load(os.path.join('resources', 'images', 'BeatLinePointer.png'))
        self.pointer_image.set_colorkey((255, 255, 255))
        self.pointer_image = pygame.transform.scale(self.pointer_image, pointer_size)

    def __init__(self, pos: tuple[int, int], width: int, filename: str, timeloop: int):
        """
        passes the arguments to the Line initiation, setups images and rectangles for visualisation
        :param pos: the position (x,y) of the center of the line
        :param width: the width of the line
        :param filename: the name of the file that the line will extract beat data from
        :param timeloop: the amount of frames the beats will be visible on the line
        """
        super().__init__(pos, width, filename, timeloop)
        self.initiate_images((int(width), int(width / 26)))
        self.rect = self.image.get_rect()
        self.pointer_rect = self.pointer_image.get_rect()

    def render(self, screen: pygame.Surface):
        """
        renders the line, beats and pointer on the screen
        :param screen:
        :return: None
        """
        self.rect.center = self.pos
        self.pointer_rect.center = self.pos
        screen.blit(self.image, self.rect)
        for beat in self.beats:
            if beat.time <= self.time + self.timeloop / 2:
                beat.render(screen)
        screen.blit(self.pointer_image, self.pointer_rect)


class Beat:
    """A singular beat on a line"""

    def __init__(self, line, time, timeframe):
        """
        :param line: parent BeatLine of the beat
        :param time: the amount of milliseconds this beat should become centered after, from the start of the song
        :param timeframe: the amount of milliseconds this beat will be active for
        """
        self.line = line
        self.step = line.width / line.timeloop  # the amount of pixels the beat should travel in 1 sec, type float
        self.time = time
        self.timeframe = timeframe
        self.x = self.line.pos[0] + int(self.step * (self.time - self.line.time))
        self.y = self.line.pos[1]
        self.active = True  # whether the beat can be used to perform an action (beat.deactivate sets this to false)

    def is_active(self):
        """
        checks whether the beat is active by comparing the time difference between it and the BeatLine to the timeframe
        :return: bool
        """
        return self.active and abs(self.time - self.line.time) < self.timeframe / 2

    def deactivate(self):
        """prevents the beat from being active in the future"""
        self.active = False

    def update(self):
        """
        updates the position of the beat
        """
        self.x = self.line.pos[0] + int(self.step * (self.time - self.line.time))


class DrawableBeat(Beat):

    def initiate_images(self, size: tuple[int, int] = (10, 40)):
        """
        unpacks&resizes images from files
        :param size: size(width, height) of the beat
        """
        self.image = pygame.image.load(os.path.join('resources', 'images', 'Beat.png'))
        self.image = pygame.transform.scale(self.image, size)
        self.image.set_colorkey((255, 255, 255))

        self.active_image = pygame.image.load(os.path.join('resources', 'images', 'BeatActive.png'))
        self.active_image = pygame.transform.scale(self.active_image, size)
        self.active_image.set_colorkey((255, 255, 255))

        self.background_image = pygame.image.load(os.path.join('resources', 'images', 'BeatActiveBackground.png'))
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (int(self.step * self.timeframe), size[1]))
        self.background_image.set_colorkey((255, 255, 255))

    def __init__(self, line, time, timeframe, size=(10, 40)):
        super().__init__(line, time, timeframe)
        self.initiate_images(size)
        self.rect = self.image.get_rect()
        self.active_rect = self.active_image.get_rect()
        self.background_rect = self.background_image.get_rect()

    def render(self, screen):
        self.rect.center = (self.x, self.y)
        self.active_rect.center = (self.x, self.y)
        self.background_rect.center = (self.x, self.y)
        screen.blit(self.background_image, self.background_rect)
        if self.is_active():
            screen.blit(self.active_image, self.active_rect)
        else:
            screen.blit(self.image, self.rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    beatline = DrawableLine((400, 300), 320, 'Opening Animal Crossing.mp3.txt', 1000)
    clock = pygame.time.Clock()
    FPS = 60
    finished = False

    pygame.mixer.music.load(os.path.join('resources', 'music', 'Opening Animal Crossing.mp3'))
    pygame.mixer.music.play()
    score = 1
    while not finished:
        screen.fill((255, 255, 255))
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if beatline.is_active():
                        print(score)
                        score += 1

        beatline.update()
        beatline.render(screen)

        pygame.display.update()