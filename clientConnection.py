from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from errors import *
from queue import Queue
from gameState import Player
from clientSender import *
from gameBoard import *

this_file = "clientConnection.py"

class receiver():

    def __init__(self, sock, gamestate, gameboard):
        
        self.sock = sock
        self.__thread = threading.Thread(target=self.__threadFunction, args=())
        self.__thread.daemon = True
        self.__thread.start()
        self.inbox = Queue()
        self.gamestate = gamestate
        self.p1 = None
        self.p2 = None
        self.gameboard = gameboard

    def __threadFunction(self) -> None:
        
        
        while not (gameClosedEvent.is_set() or connClosedEvent.is_set()):

            try:
                serverPacket= self.sock.recv(MAX_MESSAGE_SIZE)
        
                if serverPacket:
                    str = serverPacket.decode('ascii')
                    msgs = str.split()
                    for msg in msgs:       
                        self.parseMessage(msg)
                else:
                    break
            
            except:
                # No message received this time.
                pass


    
    def parseMessage (self, message: str) -> bool:
        print("RECEIVED::::", message)
        
        instruction = ""
        i = 0
        while message[i] != ':':
            if message[i] != '[':
                instruction += message[i]
            i+=1

        
        
        if message == "[Clr:BLUE]":
            self.player = self.gamestate.player
            self.player.set_as_player()
            self.gamestate.opponent.set_as_opponent()
            self.gamestate.opponent.end_turn()

            self.player.set_colour("blue")
            self.gamestate.opponent.set_colour("red")

        if message == "[Clr:RED]":
            self.player = self.gamestate.player
            self.player.set_as_player()
            self.gamestate.opponent.set_as_opponent()
            self.gamestate.opponent.end_turn()

            self.player.set_colour("red")
            self.gamestate.opponent.set_colour("blue")

        if message == "[Turn:YOU]":
            self.gamestate.player.start_turn()


        if message == "[Turn:OPP]":
            self.gamestate.player.end_turn()

        if message == "[Board:INIT]":
            self.intializeBoards()

        if instruction == "Move":
            coords = []
            for c in message:
                if c.isnumeric():
                    coords.append(int(c))

            oldSpace = self.gameboard.get_space(coords[0],coords[1])
            newSpace = self.gameboard.get_space(coords[2],coords[3])
            unit = oldSpace.get_unit()

            self.gameboard.move_unit(True,unit, newSpace)
            return True
            
        if instruction == "Kill":
            coords = []
            for c in message:
                if c.isnumeric():
                    coords.append(int(c))

            target_space = self.gameboard.get_space(coords[0],coords[1])
            target = target_space.get_unit()
            target.die()
            target_space.assign_unit(None)
            return True
        
            
        if instruction == "Hp":
            inputs = []
            for c in message:
                if c.isnumeric():
                    inputs.append(int(c))

            target_space = self.gameboard.get_space(inputs[0],inputs[1])
            target = target_space.get_unit()
            target.take_damage(inputs[2])
            target.update_stats_panel(target) 

            return True

    def setPlayerColours(self, playerColour: str, opponentColour: str):
                    
        print("Setting player to: ", playerColour)

        print("Player get_colour()", self.player.get_colour())

    def intializeBoards(self):
        self.gamestate.setup_board()
        self.opponent.setup_board()

    def killConnection(self):
        setConnClosed()

# End of receiver class.
    


def establishConn(ip, port) -> tuple[bool, socket.socket]:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        sock.settimeout(TIMEOUT_LENGTH)

    except:
        errorMessage(this_file, "Could not establish connection.")
        setConnClosed()
        return False, None

    setConnOpen()
    print("Connected to server.")
    return True, sock


