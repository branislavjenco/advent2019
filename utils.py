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

    print("Tests passed")


def get_param_mode(index, ins):
    ins = ins // 100  # remove the opcode
    mode = ins % 10
    ins = ins // 10
    for i in range(index - 1):
        mode = ins % 10
        ins = ins // 10
    return mode


def get_param(ins, program, ic, index):
    mode = get_param_mode(index, ins)
    if mode == 0:
        return program[program[ic + index]]
    elif mode == 1:
        return program[ic + index]


def run(program, input, debug=False):
    """
    Runs an intcode program
    program is a list of ints
    """
    ic = 0 # instruction counter
    output = None
    while True:
        ins = program[ic]
        op = ins % 100
        if debug:
            print("ic: %d opcode: %d" % (ic, op))
        if op == 99:
            return output
        if op == 1:
            program[program[ic + 3]] = get_param(ins, program, ic, 1) + get_param(ins, program, ic, 2)
            ic = ic + 4
        elif op == 2:
            program[program[ic + 3]] = get_param(ins, program, ic, 1) * get_param(ins, program, ic, 2)
            ic = ic + 4
        elif op == 3:
            program[program[ic + 1]] = input
            ic = ic + 2
        elif op == 4:
            output = get_param(ins, program, ic, 1)
            ic = ic + 2
        elif op == 5:
            if get_param(ins, program, ic, 1) != 0:
                ic = get_param(ins, program, ic, 2)
            else:
                ic = ic + 3
        elif op == 6:
            if get_param(ins, program, ic, 1) == 0:
                ic = get_param(ins, program, ic, 2)
            else:
                ic = ic + 3
        elif op == 7:
            if get_param(ins, program, ic, 1) < get_param(ins, program, ic, 2):
                program[program[ic + 3]] = 1
            else:
                program[program[ic + 3]] = 0
            ic = ic + 4
        elif op == 8:
            if get_param(ins, program, ic, 1) == get_param(ins, program, ic, 2):
                program[program[ic + 3]] = 1
            else:
                program[program[ic + 3]] = 0
            ic = ic + 4
        else:
            raise Exception("shouldn't happen")
