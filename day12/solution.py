from utils import file_into_list
import math
from operator import add
import itertools
import re

pattern = "^\<x=(-?\d+), y=(-?\d+), z=(-?\d+)\>$"
r = re.compile(pattern)
_input = file_into_list("day12/input.txt", map_f=lambda x: list(map(int, r.match(x).groups())))
test_input = file_into_list("day12/test_input.txt", map_f=lambda x: list(map(int, r.match(x).groups())))


class Body:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def update_position(self):
        self.position = list(map(add, self.position, self.velocity))

    @property
    def pot(self):
        return abs(self.position[0]) + abs(self.position[1]) + abs(self.position[2])

    @property
    def kin(self):
        return abs(self.velocity[0]) + abs(self.velocity[1]) + abs(self.velocity[2])

    @property
    def tot(self):
        return self.pot * self.kin

    def get_history_record(self, axis):
        return str(self.position[axis]) + "." + str(self.velocity[axis])

    def __repr__(self):
        return f"Position {self.position}. Velocity {self.velocity}"


def part_1(data):
    moons = list(map(lambda x: Body(x), data))
    combinations = list(itertools.combinations([0, 1, 2, 3], 2))
    for i in range(100):
        # apply gravity
        velocity_deltas = [[0, 0, 0] for moon in moons]
        for pair in combinations:
            for axis in range(3):
                if moons[pair[0]].position[axis] > moons[pair[1]].position[axis]:
                    velocity_deltas[pair[0]][axis] = velocity_deltas[pair[0]][axis] - 1
                    velocity_deltas[pair[1]][axis] = velocity_deltas[pair[1]][axis] + 1
                elif moons[pair[0]].position[axis] < moons[pair[1]].position[axis]:
                    velocity_deltas[pair[0]][axis] = velocity_deltas[pair[0]][axis] + 1
                    velocity_deltas[pair[1]][axis] = velocity_deltas[pair[1]][axis] - 1
        for j in range(len(moons)):
            moons[j].velocity = list(map(add, moons[j].velocity, velocity_deltas[j]))
            # apply velocity
        for moon in moons:
            moon.update_position()

    print(sum(map(lambda x: x.tot, moons)))


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def part_2(data):
    moons = list(map(lambda x: Body(x), data))
    combinations = list(itertools.combinations([0, 1, 2, 3], 2))
    history = set()
    periods = [0, 0, 0]
    for axis in range(3):
        for i in range(1000000):
            # apply gravity
            velocity_deltas = [0 for moon in moons]
            for pair in combinations:
                if moons[pair[0]].position[axis] > moons[pair[1]].position[axis]:
                    velocity_deltas[pair[0]] = velocity_deltas[pair[0]] - 1
                    velocity_deltas[pair[1]] = velocity_deltas[pair[1]] + 1
                elif moons[pair[0]].position[axis] < moons[pair[1]].position[axis]:
                    velocity_deltas[pair[0]] = velocity_deltas[pair[0]] + 1
                    velocity_deltas[pair[1]] = velocity_deltas[pair[1]] - 1
            for idx, moon in enumerate(moons):
                moon.velocity[axis] = moon.velocity[axis] + velocity_deltas[idx]
            # apply velocity
            for moon in moons:
                moon.update_position()

            record = "|".join([moon.get_history_record(axis) for moon in moons])
            if record in history:
                periods[axis] = i
                break

            history.add(record)
    return lcm(lcm(periods[0], periods[1]), periods[2])


print(part_2(_input))

