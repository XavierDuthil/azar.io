import utils
import math
import settings
from pygame.locals import Rect


class Cell:
    def __init__(self, bubble):
        self.owner = bubble
        self.rect = Rect((0, 0), (0, 0))
        self.neighbors = []
        self.local_forces = []
        self.speed = 0
        self.direction = 0

    # def pull_neighbors(self):
    #     for neighbor in neighbors:
    #         neighbor.forces_applied.append(())

    def calculate_local_forces(self):
        # Gravitation around the bubble
        direction, distance = utils.get_vector(self.owner.rect.center, self.rect.center)

        wanted_gravitation_distance = self.owner.radius
        gravitation_pull_or_push = wanted_gravitation_distance - distance
        self.local_forces.append((direction, gravitation_pull_or_push / 1000 * settings.CELL_GRAVITATION_FORCE))

        # Neighbor cells pull
        for neighbor in self.neighbors:
            direction, distance = utils.get_vector(self.rect.center, neighbor.rect.center)
            self.local_forces.append((direction, distance / 1000 * settings.CELL_MUTUAL_ATTRACTION_FORCE))

    def apply_forces(self):
        # Adding all the force vectors
        force = self.local_forces[0]
        x_movement = math.sin(force[0]) * force[1]
        y_movement = math.cos(force[0]) * force[1]

        for force in self.local_forces[1:]:
            x_movement += math.sin(force[0]) * force[1]
            y_movement += math.cos(force[0]) * force[1]

        final_movement = utils.get_vector((0, 0), (x_movement, y_movement))
        self.direction = final_movement[0]
        self.speed = final_movement[1]

        self.local_forces = []
