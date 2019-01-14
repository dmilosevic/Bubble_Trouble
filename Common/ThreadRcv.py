from PyQt5.QtCore import QThread, pyqtSignal
from multiprocessing import Queue
#from Server import *


class ThreadRcv(QThread):
    #receivedMsg = pyqtSignal(int)

    def __init__(self, socket,indicator):
        super().__init__()
        self.socket = socket
        self.queue = None
        self.returnMsg = None
        self.indicator = indicator
    def run(self):
        while True:
            text = ''
            while True:
                bin = self.socket.recv(1024)
                text += str(bin, 'utf8')
                if not bin or len(bin) < 1024:
                    break
            if len(text) != 0:
                #print('Received: ' + text)
                #print(text)
                if self.indicator == 'server':
                    textarray = text.split('|')
                    for t in textarray:
                        if t != '':
                            self.queue.put(t)
                if self.indicator == 'client':
                    #print('usao')
                    self.queue.put(text)
                #if self.parent is not None:
                    #self.parent.receivedMsg.emit(1806)
            if(self.indicator == 'client'):
                self.msleep(20)
            if self.indicator == 'server':
                self.msleep(1)
