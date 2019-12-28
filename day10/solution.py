from utils import test, file_into_string
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

test_input_1 = '''.#..#
.....
#####
....#
...##'''

expected_1 = 8

test_input_2 = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''

expected_2 = 33

test_input_3 = '''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.'''

expected_3 = 35

test_input_4 = '''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'''

expected_4 = 41

test_input_5 = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''

expected_5 = 210


def to_int(char):
    if char == '.':
        return 0
    elif char == '#':
        return 1
    else:
        return -1


def find_vector_norm(x1, x2):
    v = x2 - x1
    norm = np.linalg.norm(v)
    if norm == 0.0:
        return np.array([0, 0])
    v = np.round(v / norm, decimals=5)
    return v


def input_into_matrix(_input):
    return np.array([[to_int(y) for y in list(x)] for x in _input.split('\n')])


def find_station(matrix, get_coords=False):
    point_vectors = {}
    for x1, y1 in np.ndindex(matrix.shape):
        vectors = []
        if matrix[x1, y1] == 1:
            for x2, y2 in np.ndindex(matrix.shape):
                if matrix[x2, y2] == 1:
                    v = find_vector_norm(np.array([x1, y1]), np.array([x2, y2]))
                    if not np.array_equal(v, np.array([0, 0])):
                        vectors.append(v)
            unique_vectors = np.unique(np.array(vectors), axis=0)
            point_vectors[f'{x1},{y1}'] = unique_vectors
    max_length = 0
    station_coords = None
    for k, v in point_vectors.items():
        if len(v) > max_length:
            max_length = len(v)
            station_coords = np.fromstring(k, sep=',')
    if get_coords:
        return max_length, station_coords
    else:
        return max_length


test(lambda x: find_station(input_into_matrix(x)),
     [test_input_1, test_input_2, test_input_3, test_input_4, test_input_5],
     [expected_1, expected_2, expected_3, expected_4, expected_5])

_input = file_into_string("day10/input.txt")
field = input_into_matrix(_input)
asteroids_seen, station_coords = find_station(field, get_coords=True)


def shift_list_to_90(angles):
    """
    Shifts the list of angles in interval [-180, 180] to start at -90
    The interval [-180, -90] is then added at the end of the new list
    :param angles: list of angles
    :return: list of angles
    """
    start = None
    for i in range(len(angles)):
        if angles[i] > -90.0:
            start = i - 1
            break

    return angles[start:] + angles[:start]


def destroy_asteroids(matrix, station_coords):
    """
    Loops through the entire asteroid field and computes
    the vector between each asteroid and the given station coordinates
    Also computes the magnitude and angle.
    Stores into a dictionary where the keys are the angles. Each value
    is a list of vectors that share this angles (list of asteroids in a single
    line coming from the station coordinates) sorted by magnitude
    :param matrix:
    :param station_coords:
    :return: dictionary with angles of vectors between station coordinates
    and the asteroids
    """
    angles = {}
    x1 = int(station_coords[0])
    y1 = int(station_coords[1])
    matrix[x1, y1] = 2
    for x2, y2 in np.ndindex(matrix.shape):
        if matrix[x2, y2] == 1:
            # is asteroid
            v = np.array([x2, y2]) - np.array([x1, y1])
            magnitude = np.linalg.norm(v)
            if magnitude == 0.0:
                continue
            angle = (np.arctan2(v[0], v[1])) * 180 / np.pi
            if angles.get(angle) is None:
                angles[angle] = [((x2, y2), magnitude, v)]
            else:
                angles[angle].append(((x2, y2), magnitude, v))
    for k in angles.keys():
        angles[k] = sorted(angles[k], key=lambda tup: tup[1])

    sorted_angles = sorted(angles.keys())
    sorted_angles = shift_list_to_90(sorted_angles)
    # since the total length of the angles is more than 200, we
    # dont do a full 360 loop around the station to get to the
    # 200th asteroid, so we dont have to care about asteroids
    # that were originally occluded in the first loop
    print(angles[sorted_angles[199]])


test_field = input_into_matrix(_input)

destroy_asteroids(test_field, station_coords)
