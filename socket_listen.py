# Echo server program
import socket
from PyQt5.QtCore import QThread, QObject


class ListenSocket(QObject):

        def __init__(self):
            super().__init__()
            self.thread = QThread()
            self.moveToThread(self.thread)
            self.thread.started.connect(self.receive)
            self.s = None
            self.conn = None
            self.addr = None

        def start(self):
            # Start the thread
            self.thread.start()

        def receive(self):
            HOST = ''  # Symbolic name meaning all available interfaces
            PORT = 50005  # Arbitrary non-privileged port
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((HOST, PORT))
            self.s.listen(1)
            while True:
                self.conn, self.addr = self.s.accept()
                text = ''
                while True:
                    bin = self.conn.recv(1024)
                    text += str(bin, 'utf8')
                    if not bin or len(bin) < 1024:
                        break
                if len(text) != 0:
                    # primljena komanda
                    pass
                self.thread.msleep(5)
