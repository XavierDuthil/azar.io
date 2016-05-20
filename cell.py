import utils
import math
import settings
from pygame.locals import Rect


class Cell:
    def __init__(self, bubble, angle):
        self.owner = bubble
        self.rect = Rect((0, 0), (0, 0))
        self.neighbors = []
        self.local_forces = []
        self.speed = 0
        self.direction = 0
        self.angle = angle

    # def pull_neighbors(self):
    #     for neighbor in neighbors:
    #         neighbor.forces_applied.append(())

    def calculate_local_forces(self):
        # Gravitation pull toward resting cell position (at the right angle and distance)
        resting_position = (self.owner.rect.x + math.cos(self.angle) * self.owner.radius, self.owner.rect.y + math.sin(self.angle) * self.owner.radius)
        direction, distance = utils.get_vector(self.rect.center, resting_position)

        # Reinforced force if close
        if distance <= 50:
            gravitation_pull = 50 * distance
        else:
            gravitation_pull = math.copysign(distance ** 2, distance)
        self.local_forces.append((direction, gravitation_pull / 1000 * settings.CELL_GRAVITATION_FORCE))

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
