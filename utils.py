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
