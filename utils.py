import random
import math
import operator


def random_color():
    r = random.randint(0, 200)
    g = random.randint(0, 200)
    b = random.randint(0, 200)
    return (r, g, b)


def random_coordinates(maxWidth, maxHeight):
    x = random.randint(0, maxWidth)
    y = random.randint(0, maxHeight)
    return (x, y)


def get_vector(source_position, target_position):
    vector = tuple(map(operator.sub, source_position, target_position))

    # Calculate position differences
    xDiff = vector[0]
    yDiff = vector[1]

    # Calculate direction toward mousePos
    if yDiff == 0:
        direction = math.copysign(math.pi / 2, xDiff)
        direction += math.pi
    else:
        direction = math.atan(xDiff / yDiff)
        if yDiff > 0:
            direction += math.pi

    # Convert to Degrees
    # direction_degrees = direction * 180 / math.pi

    # Calculate distance
    if xDiff == 0 and yDiff == 0:
        distance = 0
    else:
        distance = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))

    return direction, distance
