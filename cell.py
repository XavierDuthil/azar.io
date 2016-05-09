import utils
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
        direction, distance = utils.get_vector(self.rect.center, self.owner.rect.center)

        wanted_gravitation_distance = self.owner.radius
        gravitation_pull_or_push = wanted_gravitation_distance - distance
        self.local_forces.append((direction, gravitation_pull_or_push / 10))

        # Neighbor cells pull
        for neighbor in self.neighbors:
            direction, distance = utils.get_vector(self.rect.center, neighbor.rect.center)
            self.local_forces.append((direction, distance))

    def apply_forces(self):
        self.direction = self.local_forces[0][0]
        self.speed = self.local_forces[0][1]

        # TODO : delete the two lines ahead, then add all the forces together
        self.local_forces = []
