from utils import load_intcode, IntcodeComputer, print_mat
import random
import time
import random
import numpy as np

program = load_intcode("day15/input.txt")

north = 1
south = 2
west = 3
east = 4

directions = {north, south, west, east}

wall = 0
space = 1
oxygen_system = 2

start_mark = 7
unknown_mark = 0
space_mark = 1
wall_mark = 4
oxygen_system_mark = 2


def north_of(pos):
    return [pos[0], pos[1] - 1]


def south_of(pos):
    return [pos[0], pos[1] + 1]


def west_of(pos):
    return [pos[0] - 1, pos[1]]


def east_of(pos):
    return [pos[0] + 1, pos[1]]


def dir_of(dir, pos):
    if dir == north:
        return north_of(pos)
    elif dir == south:
        return south_of(pos)
    elif dir == west:
        return east_of(pos)
    elif dir == east:
        return west_of(pos)


def opposite_of(dir):
    if dir == north:
        return south
    elif dir == south:
        return north
    elif dir == west:
        return east
    elif dir == east:
        return west


class State:
    def __init__(self, room_size):
        self.room = np.zeros([room_size, room_size], dtype=np.int)
        self.pos = [room_size // 2, room_size // 2]
        self.start_pos = self.pos
        self.path = [self.pos]
        self.prev_pos = self.pos
        self.res = space
        self.prev_res = space
        self.cmd = north
        self.prev_cmd = north

        self.room[self.pos[0], self.pos[1]] = start_mark
        self.target_pos = [self.start_pos[0] - 12, self.start_pos[1] - 12]

    def __repr__(self):
        return f"""Pos:{self.pos}
Cmd:{self.cmd}
Res:{self.res}"""


def get_pixel_neighbourhood(pos, room):
    neighborhood = {
        north: room[tuple(north_of(pos))],
        south: room[tuple(south_of(pos))],
        west: room[tuple(west_of(pos))],
        east: room[tuple(east_of(pos))]
    }
    return neighborhood


def find_empty_positions(neighborhood):
    result = []
    for k, v in neighborhood.items():
        if v == unknown_mark:
            result.append(k)
    return result


# def new_pos_to_cmd(old_pos, new_pos):
#     cmd = -1
#     if new_pos == [old_pos[0], old_pos[1] - 1]:
#         cmd = north
#     elif new_pos == [old_pos[0], old_pos[1] + 1]:
#         cmd = south
#     elif new_pos == [old_pos[0] - 1, old_pos[1]]:
#         cmd = west
#     elif new_pos == [old_pos[0] + 1, old_pos[1]]:
#         cmd = east
#     return cmd


def get_ideal_direction(curr_pos, target_pos):
    choices = []
    if curr_pos[0] > target_pos[0]:
        choices.append(west)
    elif curr_pos[0] < target_pos[0]:
        choices.append(east)
    if curr_pos[1] > target_pos[1]:
        choices.append(north)
    elif curr_pos[1] < target_pos[1]:
        choices.append(south)
    return random.choice(choices)


def set_command(state):

    cmd = get_ideal_direction(state.pos, state.target_pos)
    potential_position = dir_of(cmd, state.pos)
    if state.room[tuple(potential_position)] == wall_mark:
        cmd = random.choice(directions.difference({cmd}))
    #
    # n = get_pixel_neighbourhood(state.pos, state.room)
    # empty_positions_cmds = find_empty_positions(n)
    # if len(empty_positions_cmds) > 0:
    #     if north in empty_positions_cmds and east in empty_positions_cmds:
    #         cmd = random.choice([north, west])
    #     else:
    #         cmd = random.choice(empty_positions_cmds)
    # else:
    #     while True:
    #         cmd = get_ideal_direction(state.pos, state.target_pos)
    #         potential_position = dir_of(state.pos, cmd)
    #         if state.room[potential_position[0], potential_position[1]] == 0:
    #             break
    #
    #         cmd = random.choice([east, south])
    #         potential_position = dir_of(state.pos, cmd)
    #         if state.room[potential_position[0], potential_position[1]] == 0:
    #             break
    #         if state.room[potential_position[0], potential_position[1]] != 4:
    #             break
    state.cmd = cmd
    return state


def signal_robot(state, remote_control):
    response = remote_control.run(state.cmd)
    state.res = response
    return state


def sync_position(state):
    if state.res == space or state.res == oxygen_system:
        new_pos = get_new_position(state.pos, state.cmd)
        state.prev_pos = state.pos
        state.pos = new_pos
        state.path.append(state.prev_pos)
    return state


def map_neighbourhood(state, remote_control):
    current_neighbourhood = get_pixel_neighbourhood(state.pos, state.room)
    for direction, value in current_neighbourhood.items():
        if value == unknown_mark:
            res = remote_control.run(direction)
            if res == space:
                state.room[tuple(dir_of(direction, state.pos))] = space_mark
                remote_control.run(opposite_of(direction))
            elif res == wall:
                state.room[tuple(dir_of(direction, state.pos))] = wall_mark
            elif res == oxygen_system:
                state.room[tuple(dir_of(direction, state.pos))] = oxygen_system_mark
    return state


def reveal_room(state):
    if state.res == space:
        state.room[state.pos[0], state.pos[1]] = 2
        state.room[state.prev_pos[0], state.prev_pos[1]] = 1
    elif state.res == wall:
        wall_position = get_new_position(state.pos, state.cmd)
        state.room[wall_position[0], wall_position[1]] = 4
    return state


def part_1():
    remote_control = IntcodeComputer(program)
    state = State(50)
    while True:
        state = map_neighbourhood(state, remote_control)
        state = set_command(state)
        state = signal_robot(state, remote_control)
        state = sync_position(state)
        state = reveal_room(state)
        # print(state)
        print_mat(state.room)
        # time.sleep(0.4)
        if state.res == 2:
            break
    state.room[state.start_pos[0], state.start_pos[1]] = 7
    print(state)


part_1()
