from figures import Cell, Point
from time import sleep

class Maze():
    def __init__(self, x1, y1, num_rows, num_columns, cell_size_x, cell_size_y, window = None):
        self._x1 = x1
        self._y1 = y1 
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._cell_size_x = cell_size_x 
        self._cell_size_y = cell_size_y
        self._window = window
        self._create_cells()

    def _create_cells(self):
        self._cells = [[None for _ in range(self._num_columns)] for _ in range(self._num_rows)]
        for row_index, row in enumerate(self._cells):
            for column_index, _ in enumerate(row):
                self._cells[row_index][column_index] = Cell(Point(row_index * self._cell_size_x + self._x1, column_index * self._cell_size_y + self._y1), Point((row_index + 1) * self._cell_size_x + self._x1, (column_index + 1) * self._cell_size_y + self._y1), self._window)
        self._break_entrances()
        if self._window == None:
            return
        self._draw_cells()

    def _break_entrances(self):
        self._cells[0][0].walls = [True, False, True, True]
        self._cells[-1][-1].walls = [True, True, True, False]

    def _draw_cells(self):
        for row in self._cells:
            for cell in row:
                cell.draw()
        self._animate()

    def _animate(self):
        while True:
            self._window.redraw()
            sleep(0.05)