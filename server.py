import socket
import threading
#import time

#Global variables
HEADER = 64
#IMPLEMENT YOUR OWN IP ADDRESS AND PORT HERE
PORT = 8080
SERVER = "dangmang.xyz"
#get your local ipv4 address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#Set up server at IP address
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)
    
#What to do when a new client connects
def handle_client(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        processString(msg)    
def processString(msg):
    filename = "/var/www/cabin/asteroid/scores.txt"
    f = open(filename, "a")
    msg = msg + "\n"
    f.write(msg)
    f.close()

    topTen(filename)

def topTen(filename):
    with open(filename, 'r') as file:
        scores = file.readlines()
    for i in range(len(scores)):
        scores[i] = int(scores[i].replace('\n' and '<br>', ''))
    scores.sort(reverse=True)

    topten = "/var/www/cabin/asteroid/topten.txt"
    f = open(topten, 'w')
    length = len(scores) if len(scores) < 10 else 10
    for i in range(length):
        f.write(str(scores[i]) + "<br>\n")
    f.close()
def start():
    server.listen()
    print(f"[LISTENING] Server online at {SERVER}.")
    while True:
        #add their conn to a list of all connections
        conn, addr = server.accept()
        #start a thread of handleclient() with each new user
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
print("[STARTING] Server is starting...")
start()

