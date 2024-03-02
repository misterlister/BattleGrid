from tkinter import Tk, BOTH, Canvas

bg_col = '#d9d9d9'
window_width = 1200
window_height = 900

class Point:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class Window:
    def __init__(self, width_val, height_val, root: Tk) -> None:
        self.__root = root
        self.__root.title("Fantactics")
        self.__root.geometry(f"{width_val}x{height_val}")
        self.__root.configure(background=bg_col)
        self.canvas = Canvas(self.__root)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background=bg_col)
        self.running = True
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
        
    def close(self):
        self.running = False

    def draw_line(self, p1: Point, p2: Point, fill_colour = "black", width: int = 2):
        self.canvas.create_line(
            p1.x, 
            p1.y, 
            p2.x, 
            p2.y, 
            fill=fill_colour, 
            width=2
        )
        self.canvas.pack()