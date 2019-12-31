from utils import load_intcode, IntcodeComputer
import os
import numpy as np
import time
import sys
np.set_printoptions(threshold=sys.maxsize)

_input = load_intcode("day13/input.txt")


def show_screen(mat):
    mat = mat.T
    buffer = ""
    sys.stdout.write( 22 * "\033[A\r")
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            buffer = buffer + str(mat[i, j])
        buffer = buffer + "\n"
    sys.stdout.write(buffer)

def setup_game(screen, computer, joystick=None):
    while not computer.is_halted():
        x = computer.run(joystick)
        if x is None:
            break
        y = computer.run(joystick)
        tile_id = computer.run(joystick)

        screen[x, y] = tile_id
        if (x == len(screen) -1) and (y == len(screen[0]) - 1) and joystick is not None:
            # finished all the setup
            # only for part 2
            break
    return screen, computer


def part_1(program):
    arcade_cabinet = IntcodeComputer(program)
    screen = np.zeros([37, 22], dtype=np.int)
    screen, arcade_cabinet = setup_game(screen, arcade_cabinet)
    print(np.unique(screen, return_counts=True))


# part_1(_input)

def get_ball_coords(matrix):
    coords = np.where(matrix == 4)
    if len(coords[0]) > 0:
        return [coords[0][0], coords[1][0]]
    else:
        return []


def get_paddle_coords(matrix):
    coords = np.where(matrix == 3)
    if len(coords[0]) > 0:
        return [coords[0][0], coords[1][0]]
    else:
        return []


def get_joystick_input(paddle_coords, ball_coords, ball_direction):
    # print(paddle_coords, ball_coords, ball_direction)
    if len(paddle_coords) < 1 or len(ball_coords) < 1:
        result = 0
    elif ball_coords[0] < paddle_coords[0]:
        result = -1
    elif ball_coords[0] > paddle_coords[0]:
        result = 1
    elif ball_coords[0] == paddle_coords[0]:
        # ball and joystick are on the same line
        # determine where to move based on the direction
        if ball_coords[1] + 1 == paddle_coords[1]:
            result = 0
        else:
            result = ball_direction

    # print("res", result)
    return result


def get_ball_direction(prev_coords, curr_coords):
    if len(prev_coords) < 1 or len(curr_coords) < 1:
        result = 0
    elif prev_coords[0] < curr_coords[0]:
        result = 1
    elif prev_coords[0] > curr_coords[0]:
        result = -1
    else:
        result = 0
    return result


def step_game(computer, screen, joystick, score):
    x = computer.run(joystick)
    if x is None:
        return computer, screen, joystick, score
    y = computer.run(joystick)
    tile_id = computer.run(joystick)

    if x == -1 and y == 0:
        score = tile_id
    else:
        screen[x, y] = tile_id
    show_screen(screen)
    return computer, screen, joystick, score


def part_2(program):
    second_program = program[:]
    second_program[0] = 2

    arcade_cabinet = IntcodeComputer(second_program)
    screen = np.zeros([37, 22], dtype=np.int)

    joystick = 1
    screen, computer = setup_game(screen, arcade_cabinet, joystick)

    score = -1
    ball_coords = []
    paddle_coords = []
    ball_direction = 0
    prev_ball_coords = []
    while True:
        # print("ball", ball_coords)
        # print("paddle", paddle_coords)
        current_ball_coords = get_ball_coords(screen)
        if len(current_ball_coords) > 0 and current_ball_coords != prev_ball_coords:
            ball_coords = current_ball_coords
            ball_direction = get_ball_direction(prev_ball_coords, ball_coords)
            prev_ball_coords = ball_coords

        current_paddle_coords = get_paddle_coords(screen)
        if len(current_paddle_coords) > 0:
            paddle_coords = current_paddle_coords
            joystick = get_joystick_input(paddle_coords, ball_coords, ball_direction)

        arcade_cabinet, screen, joystick, score = step_game(arcade_cabinet, screen, joystick, score)
        if arcade_cabinet.is_halted():
            break
    print(score)

part_2(_input)


