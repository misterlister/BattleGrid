import socket
import selectors
from constants import *
from serverConnection import *
import time


this_file = "server.py"

IP = 'localhost'
PORT = 5000  
p1Active = False
p2Active = False
sel = selectors.DefaultSelector()

def receive(conn, mask):
    data = conn.recv(MAX_MESSAGE_SIZE)
    
    if data:
        if conn.fileno() == p1ID:
            pass
            #print("Message from Player 1:")
        if conn.fileno() == p2ID:
            pass
            #print("Message from Player 2:")
        
        message = data.decode('ascii')
        msgs = message.split()
        for msg in msgs:
            parse_message(msg)

    else:
        sel.unregister(conn)
        conn.close()


def parse_message(msg):

    print("PARSED MESSAGE: ", msg)
    if msg == "[Turn:END]":
       
        if(bluePlayer.isMyTurn()):
            bluePlayer.stopTurn()
            redPlayer.startTurn()
        
        elif(redPlayer.isMyTurn):
            redPlayer.stopTurn()
            bluePlayer.startTurn()
        
        else:
            errorMessage(this_file, "It is nobodies turn!")
        



if __name__ == "__main__":

    listenSocket = socket.socket()
    listenSocket.bind((IP,PORT))
    listenSocket.listen()

    print("Server listenining at hostname: ", IP, ", port: ", PORT)    
    p1Conn, p1Addr = listenSocket.accept()
    print("P1Conn type: ", type(p1Conn))
    p1ID = p1Conn.fileno()
    sel.register(p1Conn, selectors.EVENT_READ, receive)
    p1Active = True

    print("Welcome to Fantactics. Please wait for your opponent")
    p2Conn, p2Addr = listenSocket.accept()
    p2ID = p2Conn.fileno()
    sel.register(p2Conn, selectors.EVENT_READ, receive)
    p2Active = True
    print("Welcome to Fantactics.")

    bluePlayer, redPlayer = assignColours(p1Conn, p2Conn)
    
    if not (redPlayer.stopTurn() and bluePlayer.startTurn()):
        errorMessage(this_file,"Could not assign initial turns.")
    bluePlayer
    
    bluePlayer.initializeBoard()
    redPlayer.initializeBoard()
    
    listenSocket.close() 

    while p1Active or p2Active:
        try:
            events = sel.select()
        except:
            break
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
        
    p1Conn.close() 
    p2Conn.close()

    print ('Connection Closed')