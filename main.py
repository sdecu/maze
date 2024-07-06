from tkinter import Tk, BOTH, Canvas

def main():
    win = Window(800, 600)
    start_point = Point(100, 150)
    end_point = Point(300, 350)
    line = Line(start_point, end_point)
    win.draw_line(line, "red")
    win.wait_for_close()

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.title = "Maze"
        self.canvas = Canvas(self.root, bg="grey", width = width, height = height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
        
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root.protocol()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.start_point.x, self.start_point.y,
            self.end_point.x, self.end_point.y,
            fill = fill_color, width = 2
        )

class Cell:
    def __init__(self, canvas, topx, bottomx, lefty, righty):
        self.has_left_wall = True
        self.has_right_wall= True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = topx
        self._x2 = bottomx
        self._y1 = lefty
        self._y2 = righty
        self._win = canvas

        def draw(self, topx, lefty, bottomx, righty):
            if self.has_left_wall:
                start_point = Point(self._x1, self._y1)
                end_point = Point(self._x2, self._y1)
                line = Line(start_point, end_point)
                self._win.draw(line, "red")

            if self.has_right_wall:
                start_point = Point(self._x1, self._y2)
                end_point = Point(self._x2, self._y2)
                line = Line(start_point, end_point)
                self._win.draw(line, "red")

            if self.has_top_wall:
                start_point = Point(self._x1, self._y1)
                end_point = Point(self._x1, self._y2)
                line = Line(start_point, end_point)
                self._win.draw(line, "red")

            if self.has_bottom_wall:
                start_point = Point(self._x, self._y1)
                end_point = Point(self._x2, self._y1)
                line = Line(start_point, end_point)
                self._win.draw(line, "red")
main()
