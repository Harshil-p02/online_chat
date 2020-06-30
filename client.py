import socket
import threading
import time
import os


# Enter the IP address of the server that you want to connect to. Should be same as the SERVER value of server.py
SERVER = ''
PORT = 5959
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT = '!DISCONNECT'


client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_soc.connect((SERVER, PORT))

def send_msg_to_server(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_soc.send(send_length)
    client_soc.send(message)

def receive_msg_from_server():
    while True:
        msg_len = client_soc.recv(HEADER).decode(FORMAT)
        if msg_len:
            message = client_soc.recv(int(msg_len)).decode(FORMAT)
            if message == DISCONNECT:

                client_soc.close()
                print('[SERVER] You disconnected')
                os._exit(0)
            else:
                print(message)



thread = threading.Thread(target=receive_msg_from_server)
thread.start()

while True:
    time.sleep(1)
    msg = input('>>> ')
    if msg:
        send_msg_to_server(msg)