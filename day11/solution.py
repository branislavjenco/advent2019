from utils import load_intcode, IntcodeComputer, test
import numpy as np
from matplotlib import pyplot as plt
from operator import add


# direction encoding
#   0
# 3   1
#   2
def get_new_position(position, direction, signal):
    if signal == 0:
        signal = -1
    new_direction = (direction + signal) % 4
    new_position = position
    if new_direction == 0:
        new_position = list(map(add, position, [0, 1]))
    elif new_direction == 1:
        new_position = list(map(add, position, [1, 0]))
    elif new_direction == 2:
        new_position = list(map(add, position, [0, -1]))
    elif new_direction == 3:
        new_position = list(map(add, position, [-1, 0]))

    return new_position, new_direction


def part_1():
    program = load_intcode('day11/input.txt')
    robot = IntcodeComputer(program)
    grid = np.zeros([1000, 1000])
    position = [500, 500]
    direction = 0
    painted = set()
    while not robot.is_halted():
        panel = grid[position[0], position[1]]
        to_paint = robot.run(panel)
        if to_paint is None:
            break
        grid[position[0], position[1]] = to_paint
        painted.add(tuple(position))
        turn_signal = robot.run()
        new_position, new_direction = get_new_position(position, direction, turn_signal)
        direction = new_direction
        position = new_position
    print(len(painted))


def part_2():
    program = load_intcode('day11/input.txt')
    robot = IntcodeComputer(program)
    grid = np.zeros([100, 100], dtype=np.int)
    position = [50, 50]
    grid[position[0], position[1]] = 1
    direction = 0
    while not robot.is_halted():
        panel = grid[position[0], position[1]]
        to_paint = robot.run(panel)
        if to_paint is None:
            break
        grid[position[0], position[1]] = to_paint
        turn_signal = robot.run()
        new_position, new_direction = get_new_position(position, direction, turn_signal)
        direction = new_direction
        position = new_position
    plt.matshow(grid)
    plt.show()


part_2()


