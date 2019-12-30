from utils import load_intcode, IntcodeComputer
import numpy as np

program = load_intcode("day13/input.txt")

arcade_cabinet = IntcodeComputer(program)
screen = np.zeros([100, 100], dtype=np.int)
while not arcade_cabinet.is_halted():
    x = arcade_cabinet.run()
    if x is None: break
    y = arcade_cabinet.run()
    tile_id = arcade_cabinet.run()
    screen[x, y] = tile_id

print(np.unique(screen, return_counts=True))
