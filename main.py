from tkinter import Tk, BOTH, Canvas

def main():
    win = Window(800, 600)
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

if __name__ == "__main__":
    main()
