from figures import Cell, Point, Directions, WallStates
from time import sleep
import random
import heapq

def calculate_h(row, column, dest, method = "manhattan"):
    if method == "manhattan":
        return abs(dest[0] - row) + abs(dest[1] - column)
    if method == "euclidian":
        return ((row - dest[0]) ** 2 + (column - dest[1]) ** 2) ** 0.5
    if method == "djikstra":
        return 0

class Maze():
    def __init__(self, x1, y1, num_rows, num_columns, cell_size_x, cell_size_y, window = None, method = "default", seed = None):
        self._x1 = x1
        self._y1 = y1 
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._cell_size_x = cell_size_x 
        self._cell_size_y = cell_size_y
        self._window = window
        if seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrances()
        self._break_walls_r(0, 0)
        self._reset_visited_cells()
        if method == "default":
            self._solve_r(0, 0)
        elif method == "a_star":
            self._solve_a_star()

    def _create_cells(self):
        self._cells = [[None for _ in range(self._num_columns)] for _ in range(self._num_rows)]
        for column_index, row in enumerate(self._cells):
            for row_index, _ in enumerate(row):
                self._cells[row_index][column_index] = Cell(Point(row_index * self._cell_size_x + self._x1, column_index * self._cell_size_y + self._y1), Point((row_index + 1) * self._cell_size_x + self._x1, (column_index + 1) * self._cell_size_y + self._y1), self._window)
        if self._window == None:
            return
        self._draw_cells()

    def _break_walls_r(self, row, column):
        self._cells[row][column].is_visited = True
        while True:
            next_index_list = []

            if row > 0 and not self._cells[row-1][column].is_visited:
                next_index_list.append([row-1, column])

            if column > 0 and not self._cells[row][column-1].is_visited:
                next_index_list.append([row, column-1])

            if row < self._num_rows - 1 and not self._cells[row+1][column].is_visited:
                next_index_list.append([row+1, column])

            if column < self._num_columns - 1 and not self._cells[row][column+1].is_visited:
                next_index_list.append([row, column+1])

            if len(next_index_list) == 0:
                self._draw_cell(row, column)
                return
            
            next_index = next_index_list[random.randrange(len(next_index_list))]

            if next_index[0] == row - 1:
                self._cells[row][column].walls[Directions.LEFT.value] = WallStates.OPEN.value
                self._cells[row-1][column].walls[Directions.RIGHT.value] = WallStates.OPEN.value

            if next_index[0] == row + 1:
                self._cells[row][column].walls[Directions.RIGHT.value] = WallStates.OPEN.value
                self._cells[row+1][column].walls[Directions.LEFT.value] = WallStates.OPEN.value

            if next_index[1] == column - 1:
                self._cells[row][column].walls[Directions.TOP.value] = WallStates.OPEN.value
                self._cells[row][column-1].walls[Directions.BOTTOM.value] = WallStates.OPEN.value

            if next_index[1] == column + 1:
                self._cells[row][column].walls[Directions.BOTTOM.value] = WallStates.OPEN.value
                self._cells[row][column+1].walls[Directions.TOP.value] = WallStates.OPEN.value

            self._draw_cell(row, column)
            self._draw_cell(next_index[0], next_index[1])

            self._break_walls_r(next_index[0], next_index[1])

    def _solve_r(self, row, column):
        self._animate()
        self._cells[row][column].is_visited = True
        
        if row == self._num_rows - 1 and column == self._num_columns - 1:
            return True

        if row > 0 and not self._cells[row-1][column].is_visited and not self._cells[row][column].walls[Directions.LEFT.value]:
            self._draw_line(self._cells[row][column], self._cells[row-1][column])
            result = self._solve_r(row-1, column)
            if not result:
                self._draw_line(self._cells[row][column], self._cells[row-1][column], True)  
            else:
                return result  

        if column > 0 and not self._cells[row][column-1].is_visited and not self._cells[row][column].walls[Directions.TOP.value]:
            self._draw_line(self._cells[row][column], self._cells[row][column-1])
            result = self._solve_r(row, column-1)
            if not result:
                self._draw_line(self._cells[row][column], self._cells[row][column-1], True)
            else:
                return result

        if row < self._num_rows - 1 and not self._cells[row+1][column].is_visited and not self._cells[row][column].walls[Directions.RIGHT.value]:
            self._draw_line(self._cells[row][column], self._cells[row+1][column])
            result = self._solve_r(row+1, column)
            if not result:
                self._draw_line(self._cells[row][column], self._cells[row+1][column], True)
            else:
                return result

        if column < self._num_columns - 1 and not self._cells[row][column+1].is_visited and not self._cells[row][column].walls[Directions.BOTTOM.value]:
            self._draw_line(self._cells[row][column], self._cells[row][column+1])
            result = self._solve_r(row, column+1)
            if not result:
                self._draw_line(self._cells[row][column], self._cells[row][column+1], True)
            else:
                return result

        return False
    
    def _solve_a_star(self):
        source = [0, 0]
        destination = [self._num_rows - 1, self._num_columns - 1] 

        row = source[0]
        column = source[1]
        self._cells[row][column].a_star_props.f = 0
        self._cells[row][column].a_star_props.g = 0
        self._cells[row][column].a_star_props.h = 0
        self._cells[row][column].a_star_props.parent_row = row
        self._cells[row][column].a_star_props.parent_column = column

        open_list = []
        heapq.heappush(open_list, (0.0, row, column))

        found = False

        while len(open_list) > 0 and not found:
            cell = heapq.heappop(open_list)

            row = cell[1]
            column = cell[2]
            self._cells[row][column].is_visited = True

            for direction in Directions:
                new_row = row
                if direction.value == Directions.LEFT.value:
                    new_row -= 1
                elif direction.value == Directions.RIGHT.value:
                    new_row += 1
                if new_row < 0 or new_row > self._num_rows - 1:
                    continue
                new_column = column
                if direction.value == Directions.TOP.value:
                    new_column -= 1
                elif direction.value == Directions.BOTTOM.value:
                    new_column += 1
                if new_column < 0 or new_column > self._num_columns - 1:
                    continue

                if not self._cells[row][column].walls[direction.value]:
                    self._draw_line(self._cells[row][column], self._cells[new_row][new_column], True)
                    if new_row == destination[0] and new_column == destination[1]:
                        self._cells[new_row][new_column].a_star_props.parent_row = row
                        self._cells[new_row][new_column].a_star_props.parent_column = column
                        found = True
                        break
                
                    g_new = self._cells[row][column].a_star_props.g + 1.0
                    h_new = calculate_h(row, column, destination, "manhattan")
                    f_new = g_new + h_new

                    if self._cells[new_row][new_column].a_star_props.f == float("inf") or self._cells[new_row][new_column].a_star_props.f > f_new:
                        heapq.heappush(open_list, (f_new, new_row, new_column))
                        self._cells[new_row][new_column].a_star_props.f = f_new
                        self._cells[new_row][new_column].a_star_props.g = g_new
                        self._cells[new_row][new_column].a_star_props.h = h_new
                        self._cells[new_row][new_column].a_star_props.parent_row = row
                        self._cells[new_row][new_column].a_star_props.parent_column = column

        self._draw_path(self._num_rows - 1, self._num_columns - 1)

                
    def _draw_path(self, row, column):
        parent_row = self._cells[row][column].a_star_props.parent_row
        parent_column = self._cells[row][column].a_star_props.parent_column
        self._draw_line(self._cells[row][column], self._cells[parent_row][parent_column])
        if row == 0 and column == 0:
            return
        self._draw_path(parent_row, parent_column)

    def _break_entrances(self):
        self._cells[0][0].walls[Directions.TOP.value] = WallStates.OPEN.value
        self._draw_cell(0, 0)
        self._cells[-1][-1].walls[Directions.BOTTOM.value] = WallStates.OPEN.value
        self._draw_cell(self._num_rows-1, self._num_columns-1)

    def _draw_cells(self):
        for row, row_array in enumerate(self._cells):
            for column, _ in enumerate(row_array):
                self._draw_cell(row, column)

    def _draw_cell(self, row, column):
        self._cells[row][column].draw()
        self._animate()

    def _draw_line(self, cell1, cell2, undo = False):
        cell1.draw_move(cell2, undo)
        self._animate()

    def _animate(self):
        self._window.redraw()
        sleep(1 / (self._cell_size_x * self._cell_size_y))

    def _reset_visited_cells(self):
        for row in self._cells:
            for cell in row:
                cell.is_visited = False