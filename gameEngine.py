import pygame
import sys
import math
from pygame.locals import *
from pygame.gfxdraw import *
from multiprocessing import Pool

from bubble import Bubble
from dot import Dot
from camera import Camera
import settings


class GameEngine:
    dots = []

    def __init__(self, surface):
        self.clock = pygame.time.Clock()
        self.surface = surface


    def start(self):
        # standby = True
        surface_rect = self.surface.get_rect()
        player = Bubble(surface_rect.center)

        # Camera
        camera = Camera(settings.LEVEL_WIDTH, settings.LEVEL_HEIGHT, surface_rect.width, surface_rect.height)

        # Workers pool
        # pool = Pool(settings.MAX_WORKERS)

        # Initial dots
        for i in range(settings.INITIAL_DOTS):
            self.dots.append(Dot())

        while 1:
            deltat = self.clock.tick(settings.FRAMES_PER_SECOND)

            # USER INPUT
            for event in pygame.event.get():
                if not hasattr(event, 'key'):
                    continue
                # down = event.type == KEYDOWN
                if event.key == K_ESCAPE:
                    sys.exit(0)
                # elif event.key == K_SPACE: standby = True

            # UPDATE
            # if standby: continue
            # Move player
            mouse_position = pygame.mouse.get_pos()
            player.set_movement(mouse_position)
            player.update(deltat)

            # Dot eating
            # pool.map(player.process_dot, self.dots)
            for dot in self.dots:
                if (
                    dot.rect.x > player.rect.x + player.radius or
                    dot.rect.x < player.rect.x - player.radius or
                    dot.rect.y > player.rect.y + player.radius or
                    dot.rect.y < player.rect.y - player.radius
                ):
                    continue

                distanceFromPlayer = math.sqrt((dot.rect.x - player.rect.x)**2 + (dot.rect.y - player.rect.y)**2)
                if (distanceFromPlayer <= player.radius):
                    player.eat(dot)
                    self.dots.remove(dot)

            # Dots generation
            self.dots.append(Dot())

            # RENDERING
            # Camera
            camera.update(player)

            # Background
            self.surface.fill(0xffffff)
            for xPos in range(0, int(settings.LEVEL_WIDTH / settings.GRID_GAP) + 1):
                pygame.draw.line(self.surface, 0x999999, [xPos * settings.GRID_GAP - camera.state.left, 0], [xPos * settings.GRID_GAP - camera.state.left, 5000])
            for yPos in range(0, int(settings.LEVEL_HEIGHT / settings.GRID_GAP) + 1):
                pygame.draw.line(self.surface, 0x999999, [0, yPos * settings.GRID_GAP - camera.state.top], [5000, yPos * settings.GRID_GAP - camera.state.top])

            # Visible Dots
            for dot in self.dots:
                rectRelativeToCamera = camera.apply(dot)
                if camera.isVisible(rectRelativeToCamera):
                    pygame.gfxdraw.filled_circle(self.surface, rectRelativeToCamera.x, rectRelativeToCamera.y, dot.radius, dot.color)

            # Bubbles
            rectRelativeToCamera = camera.apply(player)
            pygame.gfxdraw.aacircle(self.surface, rectRelativeToCamera.x, rectRelativeToCamera.y, player.radius, player.color)

            # Shell cells
            for cell in player.shell_cells:
                cellRelativeToCamera = camera.apply(cell)
                pygame.gfxdraw.filled_circle(self.surface, cellRelativeToCamera.x, cellRelativeToCamera.y, 5, (0, 255, 0))

            pygame.display.update()