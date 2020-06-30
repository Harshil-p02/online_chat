
FORMAT = 'utf-8'
HEADER = 64

class User:

    def __init__(self, client_soc, addr, user_name):
        self.client_soc = client_soc
        self.addr = addr
        self.user_name = user_name

    def send_msg(self, msg):
        message = msg.encode(FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        self.client_soc.send(send_len)
        self.client_soc.send(message)