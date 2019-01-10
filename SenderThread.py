from PyQt5.QtCore import *
from socket_send import *


class SenderThread(QThread):

    senderSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.socket = SendSocket()
        self.senderSignal.connect(self.prepMessage)
        self.txt2Send = ''

    def prepMessage(self, msg):
        self.txt2Send = str(msg)

    def run(self):
        while True:
            if self.txt2Send != '':
                print(self.txt2Send)
                self.socket.send(self.txt2Send)
                self.txt2Send = ''
            self.msleep(20)


