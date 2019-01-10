import socket


class SendSocket:

    def __init__(self):
        self.s = socket.socket()

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, key):  # A slot with no params
        """"print('send')
        HOST = ''  # The remote host
        PORT = 50005  # The same port as used by the server
        self.s.connect((HOST, PORT))
        text2send = 'Hello world š đ č ć ž Здраво Свете'
        self.s.sendall(text2send.encode('utf8'))
        text = ''
        while True:
            bin = self.s.recv(1024)
            text += str(bin, 'utf-8')
            if not bin or len(bin) < 1024:
                break
        print('Received', text)"""""

        print('send called')
        HOST = 'localhost'  # The remote host
        PORT = 50005  # The same port as used by the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(str(key).encode('utf8'))
            text = ''
            # while True:
            #     bin = s.recv(1024)
            #     text += str(bin, 'utf-8')
            #     if not bin or len(bin) < 1024:
            #         break
            return text
