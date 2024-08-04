from window import Window
from enum import Enum

class Direction(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1: Point, point2: Point):
        self._point1 = point1
        self._point2 = point2

    def draw(self, canvas, fill_color, width = 2):
        canvas.create_line(self._point1.x, self._point1.y, self._point2.x, self._point2.y, fill=fill_color, width=width)

class Cell:
    def __init__(self, left_top_point: Point, right_bottom_point: Point, window: Window):
        self._left_top_point = left_top_point 
        self._right_bottom_point =  right_bottom_point

        self.walls = [True, True, True, True]

        self._window = window

    def draw(self):
        right_top_point = Point(self._right_bottom_point.x, self._left_top_point.y)
        left_bottom_point = Point(self._left_top_point.x, self._right_bottom_point.y)
        for index, wall in enumerate(self.walls):
            color = "black" if wall else "white"
            match index:
                case Direction.LEFT.value:
                    self._window.draw_line(Line(left_bottom_point, self._left_top_point), color)
                case Direction.TOP.value:
                    self._window.draw_line(Line(right_top_point, self._left_top_point), color)
                case Direction.RIGHT.value:
                    self._window.draw_line(Line(right_top_point, self._right_bottom_point), color)
                case Direction.BOTTOM.value:
                    self._window.draw_line(Line(left_bottom_point, self._right_bottom_point), color)

    def get_center(self):
        return Point((self._left_top_point.x + self._right_bottom_point.x) / 2, (self._left_top_point.y + self._right_bottom_point.y) / 2)

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        center1 = self.get_center()
        center2 = to_cell.get_center()
        self._window.draw_line(Line(center1, center2), fill_color=color)
