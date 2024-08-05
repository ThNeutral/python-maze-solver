from window import Window
from figures import *
from maze import Maze

NUM_ROWS = 30
NUM_COLUMNS = 30
CELL_SIZE_X = 20
CELL_SIZE_Y = 20

OFFSET_X = 50
OFFSET_Y = 50

if __name__ == "__main__":
    window = Window(NUM_ROWS * CELL_SIZE_X + 2 * OFFSET_X, NUM_COLUMNS * CELL_SIZE_Y + OFFSET_Y * 2, "Maze")
    maze = Maze(OFFSET_X, OFFSET_Y, NUM_ROWS, NUM_COLUMNS, CELL_SIZE_X, CELL_SIZE_Y, window, "a_star")
    window.wait_for_close()