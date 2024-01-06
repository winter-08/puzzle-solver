from tkinter import Tk, BOTH, Canvas
import time
from random import seed, randrange

def main():
    win = Window(800, 600)
    #p1 = Point(10, 10)
    #p2 = Point(50, 50)
    #new_cell = Cell(p1, p2, win)
    #another_cell = Cell(Point(10, 50), Point(50, 100), win)
    #new_cell.draw_move(another_cell)
    maze = Maze(10, 10, 5, 5, 10, 10, win, 6)
    win.wait_for_close()

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Puzzle Solver"
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
        canvas.pack()

class Cell:
    def __init__(self, win = None, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._win = win
        self.visited = False

    def draw(self, x1 = None, x2 = None, y1 = None, y2 = None):
        if x1:
            self._x1 = x1
        if x2:
            self._x2 = x2
        if y1:
            self._y1 = y1
        if y2:
            self._y2 = y2
        if self._win is None:
            return
        line_left = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        line_right = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        line_top = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        line_bottom = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        if self.has_left_wall:
            line_left.draw(self._win.canvas, "red")
        else:
            line_left.draw(self._win.canvas, "black")
        if self.has_right_wall:
            line_right.draw(self._win.canvas, "red")
        else:
            line_right.draw(self._win.canvas, "black")
        if self.has_top_wall:
            line_top.draw(self._win.canvas, "red")
        else:
            line_top.draw(self._win.canvas, "black")
        if self.has_bottom_wall:
            line_bottom.draw(self._win.canvas, "red")
        else:
            line_bottom.draw(self._win.canvas, "black")


    def draw_move(self, _to_cell, undo=False):
        p1 = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        p2 = Point((_to_cell._x1 + _to_cell._x2) / 2, (_to_cell._y1 + _to_cell._y2) / 2)
        line = Line(p1, p2)
        if undo:
            line.draw(self._win.canvas, "gray")
        else:
            line.draw(self._win.canvas, "red")

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed_val = None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._visited = []
        if seed_val is None:
            seed(seed_val)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        self._cells = []
        x = self._x1
        for i in range(self._num_cols):
            self._cells.append([])
            for j in range(self._num_rows):
                self._cells[i].append(Cell(self._win))
            x += self._cell_size_x
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x = (i * self._cell_size_x) + self._x1
        y = (j * self._cell_size_y) + self._y1
        self._cells[i][j].draw(x, x + self._cell_size_x, y, y + self._cell_size_y)
        self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].draw()
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].draw()
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return
        to_visit = []
        while True:
            tmp = []
            if i - 1 >= 0:
                tmp.append((i - 1, j))
            if i + 1 < self._num_cols:
                tmp.append((i + 1, j))
            if j - 1 >= 0:
                tmp.append((i, j - 1))
            if j + 1 < self._num_rows:
                tmp.append((i, j + 1))
            for x in tmp:
                if not self._cells[x[0]][x[1]].visited:
                    to_visit.append(x)
            if len(to_visit) == 0:
                self._cells[i][j].draw()
                return
            val = randrange(0, len(to_visit))
            next_coord = to_visit[val]
            print(f"next {next_coord}")
            if i < next_coord[0]:
                self._cells[i][j].has_right_wall = False
                self._cells[next_coord[0]][next_coord[1]].has_left_wall = False
            elif i > next_coord[0]:
                self._cells[i][j].has_left_wall = False
                self._cells[next_coord[0]][next_coord[1]].has_right_wall = False
            elif j < next_coord[1]:
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_coord[0]][next_coord[1]].has_top_wall = False
            elif j > next_coord[1]:
                self._cells[i][j].has_top_wall = False
                self._cells[next_coord[0]][next_coord[1]].has_bottom_wall = False
            self._cells[i][j].draw()
            self._cells[next_coord[0]][next_coord[1]].draw()
            self._break_walls_r(next_coord[0], next_coord[1])
            #to_visit.pop(val)
            return

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False



if __name__ == "__main__":
    main()
