from graphics import Window, Point, window_height, window_width
from tkinter import Tk


default_square_size = 64
default_board_rows = 8
default_board_cols = 8
board_width = default_square_size * default_board_cols
board_height = default_square_size * default_board_rows
default_x_pos = (window_width - board_width) // 2
default_y_pos = (window_height - board_height) // 2

class GameBoard:
    def __init__(
            self,
            window: Window,
            root: Tk,
            x_start: int = default_x_pos,
            y_start: int = default_y_pos,
            num_rows: int = default_board_rows,
            num_cols: int = default_board_cols,
            square_size: int = default_square_size
                 ) -> None:
        self.window = window
        self.root = root
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_start + (num_cols * square_size) 
        self.y_end = y_start + (num_rows * square_size)
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.square_size = square_size
        self.__spaces = [[Space(i, j) for j in range(self.__num_cols)] for i in range(self.__num_rows)]
        self.draw_board()
        self.window.canvas.bind('<Button-1>',self.click)

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols
    
    def draw_board(self) -> None:
        for i in range (self.__num_rows + 1):
            y_position = (self.y_start + i * self.square_size)
            p1 = Point(self.x_start, y_position)
            p2 = Point(self.x_end, y_position)
            self.window.draw_line(p1, p2)

        for j in range (self.__num_cols + 1):
            x_position = (self.x_start + j * self.square_size)
            p1 = Point(x_position, self.y_start)
            p2 = Point(x_position, self.y_end)
            self.window.draw_line(p1, p2)

    def click(self, event):
        if event.x > self.x_start and event.x < self.x_end:
            if event.y > self.y_start and event.y < self.y_end:
                row = (event.y-self.y_start) // self.square_size
                col = (event.x-self.x_start) // self.square_size
                contents = self.check_square(row, col)
                print(f"Clicked square {row},{col}. Contents: {contents}")
                return
        print("Clicked Outside Grid")

    def check_square(self, i: int, j: int):
        if i > self.__num_rows or j > self.__num_cols:
            return "Outside Grid"
        else:
            return self.__spaces[i][j].contains()
        
    def get_space(self, i, j):
        return self.__spaces[i][j]
        
    def place_unit(self, unit, i: int, j: int) -> bool:
        if self.__spaces[i][j].contains() != None:
            return False
        self.__spaces[i][j].assign_unit(unit)
        return True

class Terrain:
    def __init__(self) -> None:
        pass
    

class Space:
    def __init__(
            self,
            row: int,
            col: int,
            terrain = None,
            unit = None,
            ) -> None:
        self.__row = row
        self.__col = col
        self.__terrain = terrain
        self.__unit = unit

    def contains(self):
        return self.__unit
    
    def assign_unit(self, unit):
        self.__unit = unit
        


