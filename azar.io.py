import pygame
import sys
import settings
from pygame.locals import *
from gameEngine import GameEngine


if __name__ == "__main__":
    # INITIALISATION
    flags = DOUBLEBUF
    resolution = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

    screen = pygame.display.set_mode(resolution, flags)
    gameEngine = GameEngine(screen)

    # CONFIGURATION
    pygame.key.set_repeat(settings.KEY_DOWN_REPEAT_DELAY_MS, settings.KEY_DOWN_REPEAT_INTERVAL_MS)

    # RUN
    gameEngine.start()
    pygame.quit()
    sys.exit()
