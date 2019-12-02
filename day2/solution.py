def file_into_list(filename, map_f=lambda x: x):
    """
    Reads a file's lines into a Python list. Can supply optional
    mapping function which is applied to every line
    """
    with open(filename, encoding="utf-8") as file:
        L = [map_f(line.strip()) for line in file]
        return L

def test(func, inputs, expected):
    """ Test a pure function on list of inputs and compare with list of expected outputs """
    if len(inputs) != len(expected):
        raise Exception("need the same number of inputs and outputs in test function")

    for input, expected in zip(inputs, expected):
        result = func(input)
        if result != expected:
            raise Exception(f"Wrong result on input {input}. Expected {expected}, got {result}")

program = list(map(lambda x: int(x), file_into_list("input.txt", lambda x: x.split(","))[0]))

def run(program):
    for i in range(0, len(program), 4):
        opcode = program[i]
        if opcode == 99:
            return program
        src1Pos = program[i+1]
        src2Pos = program[i+2]
        dstPos = program[i+3]
        if opcode == 1:
            program[dstPos] = program[src1Pos] + program[src2Pos]
        elif opcode == 2:
            program[dstPos] = program[src1Pos] * program[src2Pos]
        else:
            raise Exception("shouldn't happen")


def test_part_1():
    test(run, [[1,0,0,0,99], [2,3,0,3,99], [2,4,4,5,99,0], [1,1,1,4,99,5,6,0,99]], [[2,0,0,0,99], [2,3,0,6,99], [2,4,4,5,99,9801], [30,1,1,4,2,5,6,0,99]])

def solve_part_1(program):
    program[1] = 12
    program[2] = 2
    result = run(program)
    print(result[0])


def solve_part_2(initial_program):
    for noun in range(100):
        for verb in range(100):
            new_program = initial_program[:]
            new_program[1] = noun
            new_program[2] = verb
            result = run(new_program)
            if result[0] == 19690720:
                print(100 * noun + verb)


test_part_1()
# solve_part_1(program)
solve_part_2(program)


