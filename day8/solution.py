from utils import file_into_list, test
from matplotlib import pyplot as plt
import numpy as np
_input = file_into_list('day8/input.txt')[0]


def decode_image(_input, width, height):
    layer_total = width * height
    layers = len(_input) // layer_total
    matrix = np.zeros([width, height, layers], dtype=np.int)
    for i in range(len(_input)):
        x = i % width
        y = (i // width) % height
        z = (i // width // height) % layers
        matrix[x][y][z] = _input[i]
    return matrix


test_data = '123456789012'
expected = np.array([[[1,2,3], [4,5,6]], [[7,8,9], [0,1,2]]])


def part_1(data, width, height):
    image = decode_image(data, width, height)
    layers = image.shape[2]
    min_zeros_count = width * height + 1  # more than possible in one layer
    min_zeros_layer = None
    for l in range(layers):
        layer = image[:, :, l]
        counts = np.unique(layer, return_counts=True)
        if counts[0][0] == 0:
            if counts[1][0] < min_zeros_count:
                min_zeros_count = counts[1][0]
                min_zeros_layer = l
        else:
            min_zeros_layer = l
            break

    counts = np.unique(image[:, :, min_zeros_layer], return_counts=True)
    return counts[1][1] * counts[1][2]


test(lambda x: part_1(x, 3, 2), [test_data], [1])
print("Part 1:", part_1(_input, 25, 6))


def part2(data, width, height):
    image = decode_image(data, width, height)
    result = np.zeros([width, height])
    for i in range(width):
        for j in range(height):
            channels = image[i, j, :]
            pixel = -1
            for k in channels:
                if k == 0:
                    pixel = 0
                    break
                elif k == 1:
                    pixel = 1
                    break
                elif k == 2:
                    continue
            result[i, j] = pixel
    return result


def test_part_2():
    test_data = '0222112222120000'
    print(part2(test_data, 2, 2))


test_part_2()

output = part2(_input, 25, 6).T
plt.matshow(output)
plt.show()

