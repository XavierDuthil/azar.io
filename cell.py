import utils
import math
import settings
from pygame.locals import Rect


class Cell:
    def __init__(self, bubble, angle=None, x=None, y=None, color=None):
        self.owner = bubble
        self.rect = Rect((0, 0), (0, 0))
        self.neighbors = []
        self.local_forces = []
        self.speed = 0
        self.direction = 0
        self.color = color or (0, 255, 0)

        if angle is None:
            if x is None or y is None:
                raise Exception("invalid cell initialization: need angle or (x,y)")
            self.rect.x = x
            self.rect.y = y
            relative_x = x - bubble.rect.x
            relative_y = y - bubble.rect.y

            try:
                self.angle = ((2 * math.atan(relative_y / (relative_x + math.sqrt(relative_x ** 2 + relative_y ** 2)))) + 2 * math.pi) % (2 * math.pi)
            except ZeroDivisionError:
                self.angle = math.pi
        else:
            self.rect.x = bubble.rect.x + bubble.radius * math.cos(angle)
            self.rect.y = bubble.rect.y + bubble.radius * math.sin(angle)
            self.angle = angle

    def calculate_local_forces(self):
        # Gravitation pull toward resting cell position (at the right angle and distance)
        resting_position = (self.owner.rect.x + math.cos(self.angle) * self.owner.radius, self.owner.rect.y + math.sin(self.angle) * self.owner.radius)
        direction, distance = utils.get_vector(self.rect.center, resting_position)

        # Reinforced force if close
        if distance <= 50:
            gravitation_pull = 50 * distance
        else:
            gravitation_pull = math.copysign(distance ** 2, distance)
        self.local_forces.append((direction, gravitation_pull * settings.CELL_GRAVITATION_FORCE))

        # # Neighbor cells pull
        # for neighbor in self.neighbors:
        #     direction, distance = utils.get_vector(self.rect.center, neighbor.rect.center)
        #     self.local_forces.append((direction, distance / 1000 * settings.CELL_MUTUAL_ATTRACTION_FORCE))

        # # Neighbor cells push (when too close)
        # for neighbor in self.neighbors:
        #     direction, distance = utils.get_vector(self.rect.center, neighbor.rect.center)
        #     if distance < 2 * settings.CELL_RADIUS:
        #         self.angle += 0.001 if neighbor.angle - self.angle < 0 else -0.001
        #     self.local_forces.append((direction, distance * settings.CELL_REPULSION_FORCE))

        neighbor_angles = [neighbor.angle for neighbor in self.neighbors]

        # If first and last cells of 2*Pi, use specific behaviour
        if min(neighbor_angles) < 1 and max(neighbor_angles) > 5:
            angle_between_neighbors = ((self.neighbors[1].angle + self.neighbors[0].angle + 2 * math.pi) / 2) % (2 * math.pi)
        else:
            angle_between_neighbors = (sum([neighbor.angle for neighbor in self.neighbors]) / len(self.neighbors)) % (2 * math.pi)
        print("a: {}".format(self.neighbors[0].angle))
        print("b: {}".format(self.neighbors[1].angle))
        print("angle_between_neighbors: {}".format(angle_between_neighbors))
        self.angle = angle_between_neighbors

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
