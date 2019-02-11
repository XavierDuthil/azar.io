import pygame
import sys
import math
from pygame.locals import *
from pygame.gfxdraw import *
import time
# from multiprocessing import Pool

from bubble import Bubble
from dot import Dot
from camera import Camera
import settings


class GameEngine:
    dots = []

    def __init__(self, surface):
        self.clock = pygame.time.Clock()
        self.surface = surface
        self.player = None
        self.camera = None
        self.standby = False
        self.exit = False

    def start(self):
        # standby = True
        surface_rect = self.surface.get_rect()
        self.player = Bubble(surface_rect.center)

        # Camera
        self.camera = Camera(settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT, surface_rect.width, surface_rect.height)

        # Workers pool
        # pool = Pool(settings.MAX_WORKERS)

        # Initial dots
        for i in range(settings.INITIAL_DOTS):
            self.dots.append(Dot())

        while not self.exit:
            self.run()

    def run(self):
        deltat = self.clock.tick(settings.FRAMES_PER_SECOND)
        input_increase_size = False
        input_decrease_size = False

        # USER INPUT
        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit = True
                elif event.key == K_KP_PLUS:
                    input_increase_size = True
                elif event.key == K_KP_MINUS:
                    input_decrease_size = True
                elif event.key == K_p:
                    self.standby = not self.standby

        # UPDATE
        if self.standby:
            time.sleep(0.1)
            return

        # Interpret input
        if input_increase_size:
            self.player.volume += settings.INPUT_INCREASE_VOLUME_AMOUNT
        if input_decrease_size:
            self.player.volume -= settings.INPUT_INCREASE_VOLUME_AMOUNT
            if self.player.volume < settings.INITIAL_PLAYER_VOLUME:
                self.player.volume = settings.INITIAL_PLAYER_VOLUME

        # Move player
        mouse_position = pygame.mouse.get_pos()
        self.player.set_movement(mouse_position)
        self.player.update(deltat)

        # Dot eating
        # pool.map(player.process_dot, self.dots)
        for dot in self.dots:
            if (
                dot.rect.x > self.player.rect.x + self.player.radius or
                dot.rect.x < self.player.rect.x - self.player.radius or
                dot.rect.y > self.player.rect.y + self.player.radius or
                dot.rect.y < self.player.rect.y - self.player.radius
            ):
                continue

            distanceFromPlayer = math.sqrt((dot.rect.x - self.player.rect.x)**2 + (dot.rect.y - self.player.rect.y)**2)
            if distanceFromPlayer <= self.player.radius:
                self.player.eat(dot)
                self.dots.remove(dot)

        # Dots generation
        if len(self.dots) < settings.MAX_DOTS:
            self.dots.append(Dot())

        # RENDERING
        # Camera
        self.camera.update(self.player)

        # Background
        self.surface.fill(0xffffff)
        for xPos in range(0, int(settings.LEVEL_WIDTH / settings.GRID_GAP) + 1):
            pygame.draw.line(
                self.surface,
                0x999999,
                [xPos * settings.GRID_GAP - self.camera.state.left, 0],
                [xPos * settings.GRID_GAP - self.camera.state.left, 5000]
            )
        for yPos in range(0, int(settings.LEVEL_HEIGHT / settings.GRID_GAP) + 1):
            pygame.draw.line(
                self.surface, 0x999999,
                [0, yPos * settings.GRID_GAP - self.camera.state.top],
                [5000, yPos * settings.GRID_GAP - self.camera.state.top]
            )

        # Visible Dots
        for dot in self.dots:
            rectRelativeToCamera = self.camera.apply(dot)
            if self.camera.is_visible(rectRelativeToCamera):
                pygame.gfxdraw.filled_circle(
                    self.surface,
                    rectRelativeToCamera.x,
                    rectRelativeToCamera.y,
                    dot.radius,
                    dot.color
                )

        # Bubbles
        rectRelativeToCamera = self.camera.apply(self.player)
        pygame.gfxdraw.aacircle(
            self.surface,
            rectRelativeToCamera.x,
            rectRelativeToCamera.y,
            self.player.radius,
            self.player.color
        )

        # Shell cells
        for cell in self.player.shell_cells:
            cellRelativeToCamera = self.camera.apply(cell)

            pygame.gfxdraw.filled_circle(
                self.surface,
                cellRelativeToCamera.x,
                cellRelativeToCamera.y,
                settings.CELL_RADIUS,
                cell.color
            )


        ### TMP ###
        cell1 = self.player.shell_cells[0]
        cellRelativeToCamera = self.camera.apply(cell1)
        pygame.gfxdraw.filled_circle(
            self.surface,
            cellRelativeToCamera.x,
            cellRelativeToCamera.y,
            5,
            (0, 0, 255)
        )

        for cell in cell1.neighbors:
            cellRelativeToCamera = self.camera.apply(cell)
            pygame.gfxdraw.filled_circle(
                self.surface,
                cellRelativeToCamera.x,
                cellRelativeToCamera.y,
                5,
                (0, 255, 255)
            )

        ### TMP ###

        pygame.display.update()
