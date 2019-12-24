from utils import test, load_intcode, IntcodeComputer, log
import itertools

DEBUG = False
log = log(DEBUG)

amp_controller_program = load_intcode('day7/input.txt')


def get_thruster_output(program, phase_settings):
    amps = [IntcodeComputer(program) for phase in phase_settings]
    for i, amp in enumerate(amps):
        amp.run(phase_settings[i])
    inp = 0
    for amp in amps:
        inp = amp.run(inp)
    return inp


def test_part1():
    test_program_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    test_phase_1 = [4, 3, 2, 1, 0]
    test_program_2 = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    test_phase_2 = [0, 1, 2, 3, 4]
    test_program_3 = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31,
                      1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    test_phase_3 = [1, 0, 4, 3, 2]

    test(lambda x: get_thruster_output(*x),
         [(test_program_1, test_phase_1), (test_program_2, test_phase_2), (test_program_3, test_phase_3)],
         [43210, 54321, 65210])


# test_part1()


def part1(prog):
    permutations = list(itertools.permutations([0, 1, 2, 3, 4]))
    max_output = -1
    for phase_settings in permutations:
        output = get_thruster_output(prog, phase_settings)
        if output > max_output:
            max_output = output
    return max_output


# print(part1(amp_controller_program))


def get_thruster_output_loop(program, phase_settings):
    amps = [IntcodeComputer(program) for phase in phase_settings]
    for i, amp in enumerate(amps):
        amp.run(phase_settings[i])
    inp = 0
    while True:
        for amp in amps:
            output = amp.run(inp)
            if output is not None:
                inp = output
        if amps[len(amps) - 1].is_halted():
            break
    return inp


def test_part_2():
    test_program_1 = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                      27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    test_phase_1 = [9, 8, 7, 6, 5]
    test_program_2 = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
                      -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                      53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    test_phase_2 = [9, 7, 8, 5, 6]

    test(lambda x: get_thruster_output_loop(*x),
         [(test_program_1, test_phase_1), (test_program_2, test_phase_2)],
         [139629729, 18216])


test_part_2()


def part2(prog):
    permutations = list(itertools.permutations([5, 6, 7, 8, 9]))
    max_output = -1
    for phase_settings in permutations:
        output = get_thruster_output_loop(prog, phase_settings)
        if output > max_output:
            max_output = output

    return max_output


print(part2(amp_controller_program))