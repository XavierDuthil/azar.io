import pygame
from pygame.locals import *


class Camera(object):
    def __init__(self, width, height, levelWidth, levelHeight):
        self.state = Rect(0, 0, width, height)
        self.levelWidth = levelWidth
        self.levelHeight = levelHeight

    def apply(self, target):
        return target.rect.move(-self.state.topleft[0], -self.state.topleft[1])

    def update(self, target):
        self.state = self.track(target.rect)

    def track(self, target_rect):
        left = target_rect.left - (self.levelWidth / 2)
        top = target_rect.top - (self.levelHeight / 2)
        return Rect(left, top, self.state.width, self.state.height)

    def isVisible(self, relative_position, radius=20):
        if (
            relative_position.x < 0 - radius or
            relative_position.y < 0 - radius or
            relative_position.x > self.levelWidth + radius or
            relative_position.y > self.levelHeight + radius
        ):
            return False

        else:
            return True
