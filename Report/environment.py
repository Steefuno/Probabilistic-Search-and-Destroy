import numpy
import random


# Establishes the four types of terrain an randomly assigns their type
class Terrain:
    def __init__(self):
        self.is_target = False
        self.false_negative = 0
        self.terrain_type = self.assign_type()

    # Randomly assigns a terrain type
    def assign_type(self):
        i = random.random()
        if i <= 0.25:
            return self.flat
        elif i <= 0.5:
            return self.hilly
        elif i <= 0.75:
            return self.forest
        else:
            return self.caves

    def flat(self):
        self.false_negative = 0.1

    def hilly(self):
        self.false_negative = 0.3

    def forest(self):
        self.false_negative = 0.7

    def caves(self):
        self.false_negative = 0.9


class Environment:
    # Creates a 50x50 Environment instance
    def __init__(self):
        d = 50
        self.environment_data = numpy.array((d, d), dtype=Terrain)
        self.set_target()
        return

    # Selects a random location for the target
    def set_target(self):
        d = 50
        # Selects a random position
        pos = (random.randint(0, d - 1), random.randint(0, d - 1))

        # Places the target
        self.environment_data[pos[0]][pos[1]].is_target = True
        return

    # Queries the position and returns true/false depending on the target status
    # and the false negative rate of the terrain
    def query(self, pos):
        attempt = self.environment_data[pos[0]][pos[1]].is_target
        i = random.random()

        if attempt:
            if i > self.environment_data[pos[0]][pos[1]].false_negative:
                return True
            else:
                return False
        else:
            return False
