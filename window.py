from tkinter import Tk, BOTH, Canvas


class Window():
    def __init__(self, height, width, title = ""):
        self._height = height
        self._width = width

        self._root_widget = Tk()
        self._root_widget.title(title)
        
        self._canvas = Canvas(self._root_widget, bg="white", height=height, width=width)
        self._canvas.pack(fill=BOTH, expand=1)
        
        self._is_running = False

        self._root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root_widget.update()
        self._root_widget.update_idletasks()

    def draw_line(self, line, fill_color = "black"):
        line.draw(self._canvas, fill_color)

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()

    def close(self):
        self._is_running = False