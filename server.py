import socket
import threading
from user import User

# Enter the IP address where you want to host the server
SERVER = ''
PORT = 5959
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

users = []
user_names = []

def start():
    server.listen()
    client_soc, addr = server.accept()
    get_name = '[SERVER] Enter your user name to proceed.'
    send_msg(get_name, client_soc)
    while True:
        user_name = receive_msg(client_soc)
        if user_name != None:
            if user_name not in user_names:
                user_names.append(user_name)
                send_msg('[SERVER] Welcome to the chat!\n\n---------------------\n\n', client_soc)
                break
            else:
                send_msg(f'{user_name} has already been taken!\nPlease enter another username to continue.', client_soc)

    thread = threading.Thread(target=handle_user, args=(client_soc, addr, user_name))
    thread.start()
    for user in users:
        user.send_msg(f'[SERVER] {user_name} joined the chat')
    # print(user_name.user_name)

def send_msg(msg, client_soc):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client_soc.send(send_len)
    client_soc.send(message)

def receive_msg(client_soc):
    msg_len = client_soc.recv(HEADER).decode(FORMAT)
    if msg_len:
        message = client_soc.recv(int(msg_len)).decode(FORMAT)
        return message
    else:
        return None

def handle_user(client_soc, addr, user_name):
    user_name = User(client_soc, addr, user_name)
    users.append(user_name)
    print(users)

    connected = True
    while connected:
        message = receive_msg(client_soc)
        if message == DISCONNECT:
            user_name.send_msg('[SERVER] Are you sure you want to disconnect? (Y/n)')
            disconnect_reply = receive_msg(user_name.client_soc)
            if disconnect_reply == 'Y':
                connected = False

                send_msg(DISCONNECT, client_soc)
                message = f'[SERVER] {user_name.user_name} disconnected'
            elif disconnect_reply == 'n':
                message = None

        if message != None:
            if message[:8] != '[SERVER]':
                message = f'{user_name.user_name}:\t' + message
            for user in users:
                if user.user_name != user_name.user_name:
                    user.send_msg(message)

    print(f'Closing socket for {user_name.user_name}')
    users.remove(user_name)
    print(users)
    client_soc.close()



while True:
    start()
    for user in users:
        print(user.user_name)