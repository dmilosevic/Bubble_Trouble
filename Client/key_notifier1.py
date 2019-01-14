from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from Common.Settings import *

import time


class KeyNotifier(QObject):

    key_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.keys = []
        self.is_done = False

        self.thread = QThread()
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.__work__)

    def start(self):
        """
        Start notifications.
        """
        self.thread.start()

    def add_key(self, key):
        if key == Qt.Key_Space or key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_Shift or key == Qt.Key_A or key == Qt.Key_D:
            self.keys.append(key)

    def rem_key(self, key):
        if self.keys.__contains__(key):
            self.keys.remove(key)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        """
        A slot with no params.
        """
        while not self.is_done:
            for k in self.keys:
                self.key_signal.emit(k)
            time.sleep(PLAYER_SPEED)
