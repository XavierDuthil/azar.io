import pygame
import math
import settings
import utils

from cell import Cell
from pygame.locals import *


class Bubble:
    VIEW_CENTER = (settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

    volume = 20
    radius = 20
    maxSpeed = 10
    color = (255, 0, 0)
    shell_cells = []

    def __init__(self, position):
        # pygame.sprite.Sprite.__init__(self)
        # self.src_image = pygame.image.load(image)
        self.rect = Rect(position, (0, 0))
        self.speed = self.direction = 0

        self.generate_shell()

    def update(self, deltat):
        # Calculate speed
        self.speed = self.speedPercent * self.maxSpeed

        # Set new position
        x, y = self.rect.center
        x += -self.speed * math.sin(self.direction)
        y += -self.speed * math.cos(self.direction)

        # Handle edge collision
        x = max(0, x)
        y = max(0, y)
        x = min(settings.LEVEL_WIDTH, x)
        y = min(settings.LEVEL_HEIGHT, y)

        # Update the bubble position
        x_translation = x - self.rect.x
        y_translation = y - self.rect.y
        self.rect.center = (x, y)

        # Update shell cells positions
        for cell in self.shell_cells:
            # Set new position
            x, y = cell.rect.center
            x += x_translation
            y += y_translation

            # Apply forces
            # cell.calculate_forces()
            # cell.apply_forces()

            # Handle edge collision
            x = max(0, x)
            y = max(0, y)
            x = min(settings.LEVEL_WIDTH, x)
            y = min(settings.LEVEL_HEIGHT, y)

            # Update the cell position
            cell.rect.center = (x, y)

        # Volume loss
        if (self.volume > 50):
            self.volume -= self.volume / 30000

        # Calculate radius from volume
        self.radius = round(self.volume)

        # Calculate speed from volume

    def set_movement(self, mouse_position):
        direction, distance = utils.get_vector(mouse_position, self.VIEW_CENTER)
        self.direction = direction

        # Calculate move speed in % (relative to distance between cursor and center)
        self.speedPercent = distance / settings.MAX_SPEED_CURSOR_DISTANCE
        self.speedPercent = min(self.speedPercent, 1)

    # def process_dot(self, dot):
    #     # if (
    #     #     dot.rect.x > player.rect.x + player.radius or
    #     #     dot.rect.x < player.rect.x - player.radius or
    #     #     dot.rect.y > player.rect.y + player.radius or
    #     #     dot.rect.y < player.rect.y - player.radius
    #     # ):
    #     distanceFromBubble = math.sqrt((dot.rect.x - self.rect.x)**2 + (dot.rect.y - self.rect.y)**2)
    #     if (distanceFromBubble <= self.radius):
    #         self.eat(dot)

    def eat(self, dot):
        self.volume += dot.volume

    def generate_shell(self):
        self.shell_cells = []
        r = 8 * self.radius / 5

        number_cells = 30
        increment = 2 * math.pi / number_cells

        for i in range(0, number_cells):
            angle = increment * i

            cell_x = self.rect.x + self.radius * math.cos(angle)
            cell_y = self.rect.y + self.radius * math.sin(angle)

            cell = Cell(self)
            cell.rect = Rect((cell_x, cell_y), (0, 0))

            self.shell_cells.append(cell)

        # Set neighbors
        for index, cell in enumerate(self.shell_cells):
            previous_neighbor = self.shell_cells[(index - 1) % len(self.shell_cells)]
            next_neighbor = self.shell_cells[(index + 1) % len(self.shell_cells)]
            self.shell_cells[index].neighbors = (previous_neighbor, next_neighbor)
