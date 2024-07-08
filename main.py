from tkinter import Tk, BOTH, Canvas
import time
import random

def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 0)
    maze.solve()

    win.wait_for_close()

class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.title = "Maze"
        self.width = width
        self.height = height
        self.canvas = Canvas(self.root, bg="black", width = width, height = height)
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
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall= True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        if self.has_left_wall:
            start_point = Point(self._x1, self._y1)
            end_point = Point(self._x1, self._y2)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "red")
        else:
            start_point = Point(self._x1, self._y1)
            end_point = Point(self._x1, self._y2)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "black")

        if self.has_right_wall:
            start_point = Point(self._x2, self._y1)
            end_point = Point(self._x2, self._y2)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "red")
        else:
            start_point = Point(self._x2, self._y1)
            end_point = Point(self._x2, self._y2)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "black")

        if self.has_top_wall:
            start_point = Point(self._x1, self._y1)
            end_point = Point(self._x2, self._y1)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "red")
        else:
            start_point = Point(self._x1, self._y1)
            end_point = Point(self._x2, self._y1)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "black")
            

        if self.has_bottom_wall:
            start_point = Point(self._x1, self._y2)
            end_point = Point(self._x2, self._y2)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "red")
        else:
            start_point = Point(self._x1, self._y2)
            end_point = Point(self._x2, self._y2)
            line = Line(start_point, end_point)
            self._win.draw_line(line, "black")



    def draw_move(self, to_cell, undo=False):
        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1

        fill_color = "red"
        if undo:
            fill_color = "gray"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(line, fill_color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)


        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_right_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self,i,j):
        self._cells[i][j].visited = True
        while True:
            lst = []
           # left
            if i > 0 and not self._cells[i - 1][j].visited:
                lst.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                lst.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                lst.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                lst.append((i, j + 1))
            
            if len(lst) == 0:
                self._draw_cell(i, j)                       
                return

            dir = random.randrange(len(lst))
            next = lst[dir]

            if next[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
        # left
            if next[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
        # down
            if next[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
        # up
            if next[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next[0], next[1])              

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False


    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        #left
        if (i > 0 
            and not self._cells[i - 1][j].visited 
            and not self._cells[i][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i -1, j) == True:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        #right 
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        #up
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        #down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False

    def solve(self):
        return self._solve_r(0,0)

main()

