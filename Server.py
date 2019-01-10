from socket_listen import ListenSocket
from Menu import *
import threading
import time

listenSocket = ListenSocket()

listenSocket.start()
# sendSocket.start()

# sendSocket.send1()
listenSocket.thread.wait()
# time.sleep(100)
