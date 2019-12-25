from utils import IntcodeComputer, load_intcode


def test_part_1():
    test_program_1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    test_output_1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    test_program_2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    test_output_2 = "some 16 digit number"

    test_program_3 = [104, 1125899906842624, 99]
    test_output_3 = 1125899906842624
    c = IntcodeComputer(test_program_1)
    output = []
    while not c.is_halted():
        output.append(c.run())
    print(output)


# test_part_1()


def part1():
    program = load_intcode('day9/input.txt')
    c = IntcodeComputer(program)
    output = [c.run(1)]
    while not c.is_halted():
        output.append(c.run())
    return output


# print(part1())


def part2():
    program = load_intcode('day9/input.txt')
    c = IntcodeComputer(program)
    output = [c.run(2)]
    while not c.is_halted():
        output.append(c.run())
    return output


print(part2())
