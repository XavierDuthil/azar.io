import settings
from utils import random_color, random_coordinates
from pygame import Rect


class Dot:
    DOT_SIZE = 5

    def __init__(self, position=None):
        if not position:
            position = random_coordinates(settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT)

        self.rect = Rect(position, (0, 0))
        self.color = random_color()
        self.radius = self.DOT_SIZE
        self.volume = 1
