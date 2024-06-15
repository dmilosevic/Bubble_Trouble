import socket
from Common.ThreadSend import *
from Common.ThreadRcv import *
from multiprocessing import Queue

queueClient = Queue()


class Client(object):
    def __init__(self):
        self.HOST = '192.168.0.18'#'192.168.101.248'
        self.PORT = 50000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.sendThread = ThreadSend(self.socket, 'client')
        self.recvThread = ThreadRcv(self.socket, 'client')
        self.recvThread.queue = queueClient

    def runThreads(self):
        self.sendThread.start()
        self.recvThread.start()


