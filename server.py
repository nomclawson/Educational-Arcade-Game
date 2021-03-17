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

	topScores(filename)
	topEach(msg.replace("\n", ""))
	
def topScores(filename):
	with open(filename, 'r') as file:
		raw = file.readlines()
		scores = []
	for i in range(len(raw)):
		scores.append((raw[i].split(":")[0] , int(raw[i].split(":")[1].replace('\n' and '<br>', ''))))
	scores.sort(key=lambda x: x[1], reverse=True)
	
	topten = "/var/www/cabin/asteroid/topten.txt"
	f = open(topten, 'w')
	length = len(scores) if len(scores) < 25 else 25
	for i in range(length):
		#f.write(.split(":")[0] + " : " + str(scores[i]) + "<br>\n")
		f.write(scores[i][0] + " : " + str(scores[i][1]) + "<br>\n")
	f.close()

def topEach(msg):
	msg = msg.split(":")
	filename = "/var/www/cabin/asteroid/scores.txt"
	with open(filename, 'r') as file:
		raw = file.readlines()
		scores = []
	for i in range(len(raw)):
		if raw[i].split(":")[0] == msg[0]:
			scores.append((raw[i].split(":")[0] , int(raw[i].split(":")[1].replace('\n' and '<br>', ''))))
	scores.sort(key=lambda x: x[1], reverse=True)

	filename = f"/var/www/cabin/asteroid/players/{msg[0]}.txt"
	f = open(filename, 'w+')
	length = len(scores) if len(scores) < 25 else 25
	for i in range(length):
		#f.write(.split(":")[0] + " : " + str(scores[i]) + "<br>\n")
		f.write(scores[i][0] + " : " + str(scores[i][1]) + "<br>\n")
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

