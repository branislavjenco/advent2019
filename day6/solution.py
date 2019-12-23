from utils import test, file_into_list
import numpy as np
orbits = file_into_list("day6/input.txt")

bodies = set()
for orbit in orbits:
    orbitee, orbiter = orbit.split(")")
    bodies.add(orbitee)
    bodies.add(orbiter)

bodies = sorted(list(bodies))
reverse_bodies = {}
for idx, body in enumerate(bodies):
    reverse_bodies[body] = idx
matrix = np.zeros([len(bodies), len(bodies)], dtype=np.int)

for orbit in orbits:
    orbitee, orbiter = orbit.split(")")
    orbitee_idx = reverse_bodies[orbitee]
    orbiter_idx = reverse_bodies[orbiter]
    matrix[orbitee_idx][orbiter_idx] = 1


def part1(L, rev_L, mat):

    def count_paths(body, count):
        body_idx = rev_L[body]
        children_count = count
        for child_idx in range(len(bodies)):
            if mat[body_idx][child_idx] == 1:
                child = bodies[child_idx]
                children_count += count_paths(child, count + 1)
        return children_count

    return count_paths('COM', 0)


print(part1(bodies, reverse_bodies, matrix))


def get_path_between(start, end, matrix):
    matrix = matrix.T
    path = []
    current_node = start
    while current_node != end:
        for i in range(len(bodies)):
            if matrix[current_node][i] == 1:
                path.append(current_node)
                current_node = i

    return path


def part2(rev_L, mat):
    you_idx = rev_L['YOU']
    san_idx = rev_L['SAN']
    com_idx = rev_L['COM']
    path1 = list(reversed(get_path_between(you_idx, com_idx, mat)))
    path2 = list(reversed(get_path_between(san_idx, com_idx, mat)))

    distance = 0
    for i, body in enumerate(path1):
        if path2[i] == body:
            continue
        else:
            distance = len(path1[i:]) + len(path2[i:])
            break
    return distance


print(part2(reverse_bodies, matrix))
