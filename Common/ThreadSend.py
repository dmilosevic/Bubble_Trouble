from PyQt5.QtCore import QThread, pyqtSignal


class ThreadSend(QThread):

    senderSignal = pyqtSignal(str)

    def __init__(self, socket, indicator):
        super().__init__()
        self.socket = socket
        self.txt2Send = ''
        self.senderSignal.connect(self.prepMessage)
        self.indicator = indicator

    def prepMessage(self, msg):
        self.txt2Send = msg + '|'

    def run(self):
        while True:
            if self.txt2Send != '':
                self.socket.sendall(str(self.txt2Send).encode('utf8'))
                #print(self.txt2Send)
                self.txt2Send = ''

            if self.indicator == 'server':
                self.msleep(20)
            elif self.indicator == 'client':
                self.msleep(1)

