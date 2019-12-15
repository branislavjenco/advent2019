import math
from utils import file_into_list, test

def get_fuel_from_mass(mass):
    """ As defined in part 1 """
    return max((mass // 3) - 2, 0)

def get_fuel_from_mass_advanced(mass):
    """ As defined in part 2 """
    remaining_mass = get_fuel_from_mass(mass)
    total = remaining_mass 
    while remaining_mass > 0:
        remaining_mass = get_fuel_from_mass(remaining_mass);
        total += remaining_mass
    return total

def test_part_1():
    test(get_fuel_from_mass, [12, 14, 1969, 100756], [2, 2, 654, 33583])

def test_part_2():
    test(get_fuel_from_mass_advanced, [14, 1969, 100756], [2, 966, 50346])

module_masses = file_into_list("day1/input.txt", map_f=lambda x: int(x))
module_fuels_part1 = [get_fuel_from_mass(m) for m in module_masses]
module_fuels_part2 = [get_fuel_from_mass_advanced(m) for m in module_masses]

total_fuel_part_1 = sum(module_fuels_part1)
total_fuel_part_2 = sum(module_fuels_part2)

test_part_1()
test_part_2()
print("Total fuel needed for part 1: %d" % total_fuel_part_1)
print("Total fuel needed for part 2: %d" % total_fuel_part_2)


