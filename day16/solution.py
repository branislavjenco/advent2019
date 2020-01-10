from utils import file_into_string, test
import numpy as np

_input = file_into_string("day16/input.txt", lambda x: np.array(list(x[:-1]), dtype=np.uint8))
test_input_1 = np.array(list("12345678"), dtype=np.uint8)
phases_1 = 4
expected_1 = "01029498"
test_input_2 = np.array(list("80871224585914546619083218645595"), dtype=np.uint8)
phases_2 = 100
expected_2 = "24176176"
test_input_3 = np.array(list("19617804207202209144916044189917"), dtype=np.uint8)
phases_3 = 100
expected_3 = "73745418"
test_input_4 = np.array(list("69317163492948606335995924319873"), dtype=np.uint8)
phases_4 = 100
expected_4 = "52432133"


def get_pattern(base_pattern, position):
    result = []
    for element in base_pattern:
        for i in range(position + 1):
            result.append(element)
    return result


test(lambda x: get_pattern(x[0], x[1]), [[[0, 1, 0, -1], 0], [[0, 1, 0, -1], 1], [[0, 1, 0, -1], 2]], [[0, 1, 0, -1], [0, 0, 1, 1, 0, 0, -1, -1], [0,0,0,1,1,1,0,0,0,-1,-1,-1]])


def get_patterns(base_pattern, size):
    patterns = []
    for i in range(size):
        pattern = get_pattern(base_pattern, i)
        tiled = np.tile(pattern, size//len(pattern) + 1)
        patterns.append(tiled[1:size+1])
    return patterns


def FFT(data, phases, blocks=1, truncate=True):
    base_pattern = [0, 1, 0, -1]
    input_layer = data
    output_layer = np.zeros(len(data), dtype=np.uint8)
    size = len(data)
    for phase in range(phases):
        input_layer = input_layer * blocks
        for i in range(size):
            pattern = get_pattern(base_pattern, i)
            tiled = np.tile(pattern, size//len(pattern) + 1)
            output_layer[i] = abs(np.dot(input_layer, tiled[1:size+1])) % 10
        input_layer = output_layer
    if truncate:
        return "".join(map(str, output_layer[:8]))
    else:
        return output_layer


test(lambda x: FFT(x[0], x[1]), [[test_input_1, phases_1], [test_input_2, phases_2], [test_input_3, phases_3], [test_input_4, phases_4]], [expected_1, expected_2, expected_3, expected_4])


def part_1(data):
    return FFT(data, 100)


# print(part_1(_input))


def part_2(data):
    offset = int("".join(map(str, data[:7])))
    print(offset)
    output = np.tile(FFT(data, 100, blocks=10000, truncate=False), 10000)
    print(len(output))
    # return "".join(map(str, output))
    return "".join(map(str, output[offset:offset+8]))


test2_input_1 = np.array(list("03036732577212944063491565474664"), dtype=np.uint8)
expected_2_1 = "84462026"
test2_input_2 = np.array(list("02935109699940807407585447034323"), dtype=np.uint8)
expected_2_2 = "78725270"
test2_input_3 = np.array(list("03081770884921959731165446850517"), dtype=np.uint8)
expected_2_3 = "53553731"

test(part_2, [test2_input_1, test2_input_2, test2_input_3], [expected_2_1, expected_2_2, expected_2_3])

