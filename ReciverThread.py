from PyQt5.QtCore import *
from socket_listen import *


class ReceiverThread(QThread):

    reciverSignal = pyqtSignal(str)

    def __init__(self):
        self.socket = ListenSocket()
        self.reciverSignal.connect(self.getMessage)
        self.txt2Send = ''

    def prepMessage(self, msg):
        self.txt2Send = msg

    def run(self):
        while True:
            if self.txt2Send != '':
                self.socket.send(self.txt2Send)
                self.txt2Send = ''
