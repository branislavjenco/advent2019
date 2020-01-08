from utils import load_intcode, IntcodeComputer, print_mat
import random
import time
import random
import numpy as np

program = load_intcode("day15/input.txt")
DEBUG = False


def log(*args, **kwargs):
    if DEBUG and DEBUG is True:
        print(*args, **kwargs)


north = 1
south = 2
west = 3
east = 4

directions = {north, south, west, east}

wall = 0
space = 1
oxygen_system = 2

unknown_mark = 0
space_mark = 1
visited_space_mark = 6
current_pos_mark = 7
dead_end_mark = 3
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
        return west_of(pos)
    elif dir == east:
        return east_of(pos)


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
        self.target_pos = [self.start_pos[0] - 12, self.start_pos[1] - 12]
        self.unvisited_spaces = set()

    def __repr__(self):
        return f"""Pos:{self.pos}
Cmd:{self.cmd}
Res:{self.res}
PathLen: {len(prune_path(self.path))}"""


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
        if v == space_mark or v == unknown_mark:
            result.append(k)
    return result


def find_visited_positions(neighborhood):
    result = []
    for k, v in neighborhood.items():
        if v == visited_space_mark:
            result.append(k)
    return result


def get_ideal_direction(state):
    choices = []
    if state.pos[0] > state.target_pos[0]:
        choices.append(west)
    elif state.pos[0] < state.target_pos[0]:
        choices.append(east)
    if state.pos[1] > state.target_pos[1]:
        choices.append(north)
    elif state.pos[1] < state.target_pos[1]:
        choices.append(south)
    return random.choice(choices)


def set_command(state):
    log("Getting command")
    cmd = get_ideal_direction(state)
    log("Ideal direction:", cmd)
    potential_position = dir_of(cmd, state.pos)
    if state.room[tuple(potential_position)] in [wall_mark, dead_end_mark, visited_space_mark]:
        log("Ideal direction is a wall or dead end")
        n = get_pixel_neighbourhood(state.pos, state.room)
        other_potential_directions = find_empty_positions(n)
        if len(other_potential_directions) == 0:
            log("Backtracking", n)
            other_potential_directions = find_visited_positions(n)

        log("Other potential directions", other_potential_directions)
        if state.cmd in other_potential_directions:
            cmd = state.cmd
        else:
            cmd = random.choice(other_potential_directions)
    log("Final direction:", cmd)
    state.cmd = cmd
    return state


def signal_robot(state, remote_control):
    log("Signalling robot with", state.cmd)
    response = remote_control.run(state.cmd)
    log("Robot response", response)
    state.res = response
    return state


def sync_position(state):
    log("Syncing position")
    if state.res == space or state.res == oxygen_system:
        new_pos = dir_of(state.cmd, state.pos)
        state.prev_pos = state.pos
        state.pos = new_pos
        state.path.append(state.prev_pos)
        tuple_pos = tuple(state.pos)
        if tuple_pos in state.unvisited_spaces:
            state.unvisited_spaces.remove(tuple_pos)
    return state


def map_neighbourhood(state, remote_control):
    log("Mapping neighbourhood")
    current_neighbourhood = get_pixel_neighbourhood(state.pos, state.room)
    log(state.pos)
    log("Current neighbourhood", current_neighbourhood)
    for direction, value in current_neighbourhood.items():
        if value == unknown_mark:
            res = remote_control.run(direction)
            if res == space:
                state.room[tuple(dir_of(direction, state.pos))] = space_mark
                remote_control.run(opposite_of(direction))
                state.unvisited_spaces.add(tuple(dir_of(direction, state.pos)))
            elif res == wall:
                state.room[tuple(dir_of(direction, state.pos))] = wall_mark
            elif res == oxygen_system:
                state.room[tuple(dir_of(direction, state.pos))] = oxygen_system_mark
                remote_control.run(opposite_of(direction))
    if state.room[tuple(state.pos) == unknown_mark]:
        state.room[tuple(state.pos)] = space_mark

    log("Mapped neighbourhood", get_pixel_neighbourhood(state.pos, state.room))
    return state


def reveal_room(state):
    log("Adding visited/deadend marks")
    state.room[state.pos[0], state.pos[1]] = current_pos_mark
    prev_n = get_pixel_neighbourhood(state.prev_pos, state.room)
    if len(list(filter(lambda x: x == wall_mark or x == dead_end_mark, prev_n.values()))) > 2:
        state.room[state.prev_pos[0], state.prev_pos[1]] = dead_end_mark
    else:
        state.room[state.prev_pos[0], state.prev_pos[1]] = visited_space_mark
    return state


def prune_path(path):
    pruned_path = set()
    tuple_path = map(tuple, path)
    for point in tuple_path:
        if point not in pruned_path:
            pruned_path.add(point)
        else:
            pruned_path.remove(point)
    return pruned_path


def part_1():
    remote_control = IntcodeComputer(program)
    state = State(42)
    while True:
        log("=======Starting iteration=======")
        print_mat(state.room, [state.res, state.cmd, get_pixel_neighbourhood(state.pos, state.room)])
        # time.sleep(2)
        state = map_neighbourhood(state, remote_control)
        # print_mat(state.room)
        # time.sleep(2)
        state = set_command(state)
        state = signal_robot(state, remote_control)
        state = sync_position(state)
        # print_mat(state.room)
        # time.sleep(2)
        state = reveal_room(state)
        # print_mat(state.room)
        # print(state)
        # time.sleep(0.1)
        if state.res == 2:
            break
    state.room[state.start_pos[0], state.start_pos[1]] = current_pos_mark
    print(state)


# part_1()


def part_2():
    remote_control = IntcodeComputer(program)
    state = State(42)
    stop_flag = False
    while True:
        log("=======Starting iteration=======")
        print_mat(state.room, [state.res, state.cmd, get_pixel_neighbourhood(state.pos, state.room)])
        # time.sleep(2)
        state = map_neighbourhood(state, remote_control)
        # print_mat(state.room)
        # time.sleep(2)
        state = set_command(state)
        state = signal_robot(state, remote_control)
        state = sync_position(state)
        # print_mat(state.room)
        # time.sleep(2)
        state = reveal_room(state)
        # print_mat(state.room)
        # print(state)
        # time.sleep(0.1)


    state.room[state.start_pos[0], state.start_pos[1]] = current_pos_mark
    print(state)

part_2()