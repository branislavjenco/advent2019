from utils import IntcodeComputer, load_intcode, print_mat
import numpy as np
program = load_intcode("day17/input.txt")


def get_align_params(pos):
    return pos[0] * pos[1]


def is_intersection(pos, mat):
    if mat[pos[0], pos[1]] == 35 and mat[pos[0] - 1, pos[1]] == 35 and mat[pos[0] + 1, pos[1]] == 35 and mat[pos[0], pos[1] - 1] == 35 and mat[pos[0], pos[1] + 1] == 35:
        return True
    else:
        return False


def find_intersections(mat):
    param_sum = 0
    for i in range(1, len(mat) - 1):
        for j in range(1, len(mat[0]) - 1):
            intersect = is_intersection([i,j], mat)
            if intersect:
                param_sum += get_align_params([i, j])
    return param_sum


c = IntcodeComputer(program)

scaffold = [[]]
row = 0
while True:
    output = c.run()
    if output:
        if output == 10:
            scaffold.append([])
            row += 1
        else:
            scaffold[row].append(output)
    else:
        break
scaffold = np.array(scaffold[:-2])

print(find_intersections(scaffold))

print(print_mat(scaffold, use_ascii=True, transpose=False))