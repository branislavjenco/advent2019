from utils import file_into_string, test
import numpy as np

_input = file_into_string("day16/input.txt", lambda x: np.array(list(x[:-1]), dtype=np.int))
test_input_1 = np.array(list("12345678"), dtype=np.int)
phases_1 = 4
expected_1 = "01029498"
test_input_2 = np.array(list("80871224585914546619083218645595"), dtype=np.int)
phases_2 = 100
expected_2 = "24176176"
test_input_3 = np.array(list("19617804207202209144916044189917"), dtype=np.int)
phases_3 = 100
expected_3 = "73745418"
test_input_4 = np.array(list("69317163492948606335995924319873"), dtype=np.int)
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
        patterns.append(get_pattern(base_pattern, i))
    return patterns


def FFT(data, phases):
    base_pattern = [0, 1, 0, -1]
    patterns = get_patterns(base_pattern, len(data))
    input_layer = data
    output_layer = np.zeros(len(data), dtype=np.int)
    for phase in range(phases):
        for i in range(len(output_layer)):
            s = 0
            pattern = patterns[i]
            for j in range(len(input_layer)):
                s += input_layer[j] * pattern[(j+1) % len(pattern)]
            output_layer[i] = abs(s) % 10
        input_layer = output_layer
    return "".join(map(str, output_layer[:8]))


test(lambda x: FFT(x[0], x[1]), [[test_input_1, phases_1], [test_input_2, phases_2], [test_input_3, phases_3], [test_input_4, phases_4]], [expected_1, expected_2, expected_3, expected_4])


def part_1(data):
    return FFT(data, 100)

print(part_1(_input))
