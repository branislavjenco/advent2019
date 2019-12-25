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


def run(program, inputs, debug=False):
    """
    Runs an intcode program
    program is a list of ints
    """
    if not isinstance(inputs, list):
        inputs = [inputs]
    ic = 0  # instruction counter
    input_counter = 0
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
            ic += 4
        elif op == 2:
            program[program[ic + 3]] = get_param(ins, program, ic, 1) * get_param(ins, program, ic, 2)
            ic += 4
        elif op == 3:
            program[program[ic + 1]] = inputs[input_counter]
            input_counter += 1
            ic += 2
        elif op == 4:
            output = get_param(ins, program, ic, 1)
            ic += 2
        elif op == 5:
            if get_param(ins, program, ic, 1) != 0:
                ic = get_param(ins, program, ic, 2)
            else:
                ic += 3
        elif op == 6:
            if get_param(ins, program, ic, 1) == 0:
                ic = get_param(ins, program, ic, 2)
            else:
                ic += 3
        elif op == 7:
            if get_param(ins, program, ic, 1) < get_param(ins, program, ic, 2):
                program[program[ic + 3]] = 1
            else:
                program[program[ic + 3]] = 0
            ic += 4
        elif op == 8:
            if get_param(ins, program, ic, 1) == get_param(ins, program, ic, 2):
                program[program[ic + 3]] = 1
            else:
                program[program[ic + 3]] = 0
            ic += 4
        else:
            raise Exception("shouldn't happen")


def load_intcode(filename):
    return list(map(lambda x: int(x), file_into_list(filename, lambda x: x.split(","))[0]))


class IntcodeComputer:
    program = []
    ic = 0
    relative_base = 0

    @property
    def ins(self):
        return self.program[self.ic]

    def __init__(self, program):
        self.program = program[:] + [0]*100000

    def get_param(self, offset, write=False):
        mode = get_param_mode(offset, self.ins)
        value = None
        if mode == 0:
            value = self.program[self.ic + offset]
        elif mode == 1:
            value = self.ic + offset
        elif mode == 2:
            value = self.relative_base + self.program[self.ic + offset]

        if write:
            return value
        else:
            return self.program[value]

    def run(self, _input=None):
        output = None
        used_input = False
        while True:
            op = self.ins % 100
            print(self.ins, self.relative_base)
            if op == 99:
                break
            if op == 1:
                self.program[self.get_param(3, write=True)] = self.get_param(1) + self.get_param(2)
                self.ic += 4
            elif op == 2:
                self.program[self.get_param(3, write=True)] = self.get_param(1) * self.get_param(2)
                self.ic += 4
            elif op == 3:
                if not used_input:
                    self.program[self.get_param(1, write=True)] = _input
                    self.ic += 2
                    used_input = True
                else:
                    break
            elif op == 4:
                output = self.get_param(1)
                self.ic += 2
                break
            elif op == 5:
                if self.get_param(1) != 0:
                    self.ic = self.get_param(2)
                else:
                    self.ic += 3
            elif op == 6:
                if self.get_param(1) == 0:
                    self.ic = self.get_param(2)
                else:
                    self.ic += 3
            elif op == 7:
                if self.get_param(1) < self.get_param(2):
                    self.program[self.get_param(3, write=True)] = 1
                else:
                    self.program[self.get_param(3, write=True)] = 0
                self.ic += 4
            elif op == 8:
                if self.get_param(1) == self.get_param(2):
                    self.program[self.get_param(3, write=True)] = 1
                else:
                    self.program[self.get_param(3, write=True)] = 0
                self.ic += 4
            elif op == 9:
                self.relative_base = self.relative_base + self.get_param(1)
                self.ic += 2
            else:
                raise Exception("shouldn't happen")
        return output

    def is_halted(self):
        return self.program[self.ic] == 99


def log(debug):
    def _log(*args):
        if debug:
            print(*args)
    return _log
