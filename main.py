from tkinter import Tk, BOTH, Canvas

def main():
    win = Window(800, 600)
    p1 = Point(10, 100)
    p2 = Point(400, 600)
    new_line = Line(p1, p2)
    win.draw_line(new_line, "Red")
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

if __name__ == "__main__":
    main()
