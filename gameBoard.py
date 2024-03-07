from graphics import Window, Point, WINDOW_HEIGHT, WINDOW_WIDTH, BG_COL
from tkinter import Tk

SPRITE_BUFFER = 8
DEFAULT_SQUARE_SIZE = 64 + SPRITE_BUFFER
SELECTION_BUFFER = 3
SELECTION_SQUARE = DEFAULT_SQUARE_SIZE - SELECTION_BUFFER
BOARD_ROWS = 8
BOARD_COLS = 8
BOARD_WIDTH = DEFAULT_SQUARE_SIZE * BOARD_COLS
BOARD_HEIGHT = DEFAULT_SQUARE_SIZE * BOARD_ROWS
DEFAULT_X_POS = (WINDOW_WIDTH - BOARD_WIDTH) // 2
DEFAULT_Y_POS = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2


class GameBoard:
    def __init__(
            self,
            window: Window,
            root: Tk,
            x_start: int = DEFAULT_X_POS,
            y_start: int = DEFAULT_Y_POS,
            square_size: int = DEFAULT_SQUARE_SIZE
                 ) -> None:
        self.window = window
        self.root = root
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_start + (BOARD_COLS * square_size) 
        self.y_end = y_start + (BOARD_ROWS * square_size)
        self.square_size = square_size
        self.__spaces = [[Space(i, j) for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)]
        self.draw_board()
        self.window.canvas.bind('<Button-1>', self.click)
        self.selected_space = None
        self.selected_unit = None
        self.__valid_moves = None
    
    def draw_board(self) -> None:
        for i in range (BOARD_ROWS + 1):
            y_position = (self.y_start + i * self.square_size)
            p1 = Point(self.x_start, y_position)
            p2 = Point(self.x_end, y_position)
            self.window.draw_line(p1, p2)

        for j in range (BOARD_COLS + 1):
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
                new_space = self.__spaces[row][col]
                if self.selected_unit is None: # No unit is currently selected
                    if self.selected_space is not None:
                        if self.selected_space == new_space:
                            self.deselect_space()
                            return
                        self.deselect_space()
                    self.select_space(row, col)
                    return
                else: # A unit is currently selected
                    if new_space in self.__valid_moves:
                        self.move_unit(self.selected_unit, new_space)
                    else:
                        print("Invalid Move.")
                    self.deselect_space()
                    return

    def outline_space(self, row: int, col: int, colour: str) -> None:
        x1 = self.x_start + (col * (self.square_size)) + SELECTION_BUFFER
        y1 = self.y_start + (row * (self.square_size)) + SELECTION_BUFFER
        x2 = self.x_start + ((col+1) * (self.square_size)) - SELECTION_BUFFER
        y2 = self.y_start + ((row+1) * (self.square_size)) - SELECTION_BUFFER
        self.window.canvas.create_rectangle(x1, y1, x2, y2, width=SPRITE_BUFFER/2, outline=colour)

    def check_square(self, row: int, col: int):
        if row > BOARD_ROWS or col > BOARD_COLS:
            return "Outside Grid"
        else:
            unit = self.__spaces[row][col].get_unit()
            if unit is None:
                return unit
            return unit.get_name()
        
    def get_space(self, row, col):
        return self.__spaces[row][col]
        
    def place_unit(self, unit, row: int, col: int) -> bool:
        if self.__spaces[row][col].get_unit() != None:
            return False
        self.__spaces[row][col].assign_unit(unit)
        return True
    
    def draw_space(self, space) -> None:
        col = space.get_col()
        row = space.get_row()
        x = self.x_start + SPRITE_BUFFER/2 + (col * self.square_size)
        y = self.y_start + SPRITE_BUFFER/2 + (row * self.square_size)
        #terrain = self.__spaces[i][j].get_terrain()
        #terrain_sprite = terrain.get_sprite()
        #self.window.draw_sprite(x, y, terrain_sprite)

        ### TEMPORARY
        self.erase(row, col)
        ###

        unit = space.get_unit()
        if unit is not None:
            unit_sprite = unit.get_sprite()
            self.window.draw_sprite(x, y, unit_sprite)
        if space.is_selected():
            self.outline_space(row, col, 'blue')

    def draw_sprites(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.draw_space(self.__spaces[i][j])


###### TEMPORARY
    def erase(self, row, col):
        x1 = self.x_start + (col * (self.square_size))
        y1 = self.y_start + (row * (self.square_size))
        x2 = self.x_start + ((col+1) * (self.square_size))
        y2 = self.y_start + ((row+1) * (self.square_size))
        self.window.canvas.create_rectangle(x1, y1, x2, y2, fill=BG_COL, outline = 'black', width=2)
######

    def movement_spaces(self, i: int, j: int) -> set:
        range = self.selected_unit.get_movement()
        valid_coords = self.selected_unit.movement_spaces_r(i, j, range, self.__spaces)
        valid_spaces = []
        for tuple in valid_coords:
            self.outline_space(tuple[0], tuple[1], 'green')
            valid_spaces.append(self.__spaces[tuple[0]][tuple[1]])
        return valid_spaces

    def select_space(self, row: int, col: int) -> None:
        new_space = self.__spaces[row][col]
        new_space.select()
        self.selected_space = new_space
        self.selected_unit = new_space.get_unit()
        self.draw_space(new_space)
        if self.selected_unit is not None:
            self.__valid_moves = self.movement_spaces(row, col)

    def deselect_space(self) -> None:
        space = self.selected_space
        if space is not None:
            space.deselect()
            self.selected_space = None
            self.selected_unit = None
            self.draw_space(space)
            for sp in self.__valid_moves:
                self.draw_space(sp)
            self.__valid_moves = None

    def move_unit(self, unit, space):
        old_space = unit.get_location()
        try:  
            unit.move(space)
            self.draw_space(old_space)
            self.draw_space(space)
        except Exception as e:
            print(e)

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
        self.__selected = False

    def get_unit(self):
        return self.__unit
    
    def assign_unit(self, unit):
        self.__unit = unit

    def get_terrain(self):
        return self.__terrain
    
    def get_unit_sprite(self):
        if self.__unit == None:
            return None
        return self.__unit.get_sprite()
    
    def get_terrain_sprite(self):
        pass
    
    def get_row(self):
        return self.__row
    
    def get_col(self):
        return self.__col
    
    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False

    def is_selected(self):
        return self.__selected
