import socket
import selectors
from constants import *
from serverSend import assignColours
from serverRecv import *
from errors import errorMessage
import time


this_file = "server.py"

p1Active = False
p2Active = False
sel = selectors.DefaultSelector()

def receive(conn, mask):
    data = conn.recv(MAX_MESSAGE_SIZE)
    recvPlayer = None
    if data:
        message = data.decode('ascii')


        if conn.fileno() == bluePlayer.getID():
            recvPlayer = redPlayer
            print("***RECEIVED from BLUE: ", message)

        if conn.fileno() == redPlayer.getID():
            recvPlayer = bluePlayer
            print("***RECEIVED from RED: ", message)

        msgs = message.split()
        for msg in msgs:
            parse_message(recvPlayer,msg)

    else:
        sel.unregister(conn)
        conn.close()


def parse_message(receivingPlayer,msg):

    instruction = ""

    i = 0
    while msg[i] != ':':
        if msg[i] != '[':
            instruction += msg[i]
        i+=1

    if msg == "[Turn:END]":
       
        if(bluePlayer.isMyTurn()):
            bluePlayer.stopTurn()
            redPlayer.startTurn()
        
        elif(redPlayer.isMyTurn):
            redPlayer.stopTurn()
            bluePlayer.startTurn()
        
        else:
            errorMessage(this_file, "It is nobodies turn!")
    
    if instruction == "Move":

        coords = []

        for c in msg:
            if c.isnumeric():
                coords.append(str(c))

        relayString = "[Move:"
        translatedCoords = []
        for n in coords:
            tn = (abs(int(n)-7))
            translatedCoords.append(tn)
            
        relayString += str(translatedCoords[0]) + ',' + str(translatedCoords[1])
        relayString += ':'
        relayString += str(translatedCoords[2]) + ',' + str(translatedCoords[3])
        relayString += ']'

        receivingPlayer.sendString(relayString)

        
    if instruction == "Kill":
        coords = []
        for c in msg:
            if c.isnumeric():
                coords.append(str(c))

        relayString = "[Kill:"
        translatedCoords = []
        for n in coords:
            tn = (abs(int(n)-7))
            translatedCoords.append(tn)
        relayString += str(translatedCoords[0]) + ',' + str(translatedCoords[1])
        relayString += ']'

        receivingPlayer.sendString(relayString)

    if instruction == "Hp":

        inputs = []

        for c in msg:
            if c.isnumeric():
                inputs.append(str(c))

        relayString = "[Hp:"
        t_row = str((abs(int(inputs[0])-7)))
        t_col = str((abs(int(inputs[1])-7)))
        hp = inputs[2]

        relayString += t_row + ',' + t_col
        relayString += ':' + hp + ']'

        receivingPlayer.sendString(relayString)


if __name__ == "__main__":
    

    listenSocket = socket.socket()
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
    listenSocket.bind((IP, PORT))
    listenSocket.listen()

    print("Server listenining at hostname: ", IP, ", port: ", PORT)    
    p1Conn, p1Addr = listenSocket.accept()
    print("P1Conn type: ", type(p1Conn))
    p1Active = True

    print("Welcome to Fantactics. Please wait for your opponent")
    p2Conn, p2Addr = listenSocket.accept()
    p2Active = True
    print("Welcome to Fantactics.")

    bluePlayer, redPlayer = assignColours(p1Conn, p2Conn)
    sel.register(bluePlayer.getConn(), selectors.EVENT_READ, receive)
    sel.register(redPlayer.getConn(), selectors.EVENT_READ, receive)

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
