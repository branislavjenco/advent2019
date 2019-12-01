import math

def file_into_list(filename, map_f=lambda x: x):
    with open(filename, encoding="utf-8") as file:
        L = [map_f(line.strip()) for line in file]
        return L

def get_fuel_from_mass(mass):
    return max((mass // 3) - 2, 0)

def get_fuel_from_mass_advanced(mass):
    remaining_mass = get_fuel_from_mass(mass)
    total = remaining_mass 
    while remaining_mass > 0:
        remaining_mass = get_fuel_from_mass(remaining_mass);
        total += remaining_mass
    return total

def test(func, inputs, expected):
    if len(inputs) != len(expected):
        raise Exception("need the same number of inputs and outputs in test function")

    for input, expected in zip(inputs, expected):
        result = func(input)
        if result != expected:
            raise Exception("Wrong result on input %d. Expected %d, got %d" % (input, expected, result))

def test_part_1():
    test(get_fuel_from_mass, [12, 14, 1969, 100756], [2, 2, 654, 33583])

def test_part_2():
    test(get_fuel_from_mass_advanced, [14, 1969, 100756], [2, 966, 50346])

module_masses = file_into_list("input.txt", map_f=lambda x: int(x))
module_fuels_part1 = [get_fuel_from_mass(m) for m in module_masses]
module_fuels_part2 = [get_fuel_from_mass_advanced(m) for m in module_masses]

total_fuel_part_1 = sum(module_fuels_part1)
total_fuel_part_2 = sum(module_fuels_part2)

test_part_1()
test_part_2()
print("Total fuel needed for part 1: %d" % total_fuel_part_1)
print("Total fuel needed for part 2: %d" % total_fuel_part_2)


