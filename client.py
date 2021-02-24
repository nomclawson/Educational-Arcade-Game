import socket
import threading
import os

#global variables
HEADER = 64
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!D'
SERVER = "dangmang.xyz"
ADDR = (SERVER, PORT)

def send(msg):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(f"Sending score to {SERVER}...")
	client.connect(ADDR)

	msg = "\n" + msg + "<br>"
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)
	print(f"Score of {msg} sent to {SERVER} successfuly.")
