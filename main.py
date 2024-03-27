from tkinter import Tk
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface
from mainMenu import MainMenu
from constants import *

if __name__ == "__main__":
    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board, userInterface)
    #mainMenu = MainMenu(root)
    root.mainloop()