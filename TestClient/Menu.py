from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QImage, QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QApplication

from settings import *
from Game import SimMoveDemo, queueForCalcs, queueForResults, queueCalcLives, queueResLives
import sys
from multiprocessing import Process, Queue
from os import path
import sys

sys.path.append(path.abspath(path.join(path.dirname(__file__), '..')))

from Client.GUI import *

def pointsProcess(qCalcs: Queue, qRes: Queue):
    while True:
        if not qCalcs.empty():
            calc = str(qCalcs.get())
            id = calc.split(',')[0]
            previous = calc.split(',')[1]
            points = calc.split(',')[2]

            newPoints = int(previous)+int(points)
            qRes.put(str(newPoints))


def livesProcess(qCalcs: Queue, qRes: Queue):
    while True:
        if not qCalcs.empty():
            calc = str(qCalcs.get())
            ret = int(calc) - 1

            qRes.put(str(ret))

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(600, 200, WINDOWWIDTH, WINDOWHEIGHT)
        self.background = IMAGES_DIR + 'MenuBackground.png'

        self.__init_ui__()

    def __init_ui__(self):
        self.setWindowTitle('Bubble Trouble')
        # BACKGROUND
        oImage = QImage(self.background)
        sImage = oImage.scaled(QSize(WINDOWWIDTH, WINDOWHEIGHT))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.layout = QVBoxLayout()

        self.labelOnePlayer = self.initLabel("1 PLAYER")

        self.labelTwoPlayers = self.initLabel("2 PLAYERS")

        self.labelOnlineGame = self.initLabel("ONLINE")

        self.labelQuit = self.initLabel("CUP")

        self.labelOnePlayer.setGeometry(175, 235, 185, 35)
        self.labelTwoPlayers.setGeometry(165, 295, 185, 35)
        self.labelOnlineGame.setGeometry(192, 350, 185, 35)
        self.labelQuit.setGeometry(215, 410, 185, 35)

        self.labelOnePlayer.mousePressEvent = self.mouseClicked1P
        self.labelOnePlayer.enterEvent = self.mouseOverLabel1P
        self.labelOnePlayer.leaveEvent = self.mouseLeftLabel1P

        self.labelTwoPlayers.mousePressEvent = self.mouseClicked2P
        self.labelTwoPlayers.enterEvent = self.mouseOverLabel2P
        self.labelTwoPlayers.leaveEvent = self.mouseLeftLabel2P

        self.labelQuit.mousePressEvent = self.mouseClickedQ
        self.labelQuit.enterEvent = self.mouseOverLabelQ
        self.labelQuit.leaveEvent = self.mouseLeftLabelQ

        self.labelOnlineGame.mousePressEvent = self.mouseClickedOnline
        self.labelOnlineGame.enterEvent = self.mouseOverLabelOnline
        self.labelOnlineGame.leaveEvent = self.mouseLeftLabelOnline

        self.setLayout(self.layout)

        self.show()

    def initLabel(self, text):
        label = QLabel(text, self)
        label.setFont(QFont('Denne Kitten Heels', 25, QFont.ExtraBold))
        label.setAlignment(Qt.AlignTop)
        label.setFrameStyle(1)
        label.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")
        label.setFixedSize(QSize(185, 35))
        return label

    def mouseClicked1P(self, event):
        self.labelOnePlayer.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        process.start()
        processLives.start()
        game = SimMoveDemo(self)
        game.menuSignal.emit(1)
        self.setCentralWidget(game)
        self.labelOnePlayer.hide()
        self.labelTwoPlayers.hide()
        self.labelOnlineGame.hide()
        self.labelQuit.hide()

    def mouseOverLabel1P(self, event):
        self.labelOnePlayer.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabel1P(self, event):
        self.labelOnePlayer.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")

    def mouseClicked2P(self, event):
        self.labelTwoPlayers.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        process.start()
        processLives.start()
        game = SimMoveDemo(self)
        game.menuSignal.emit(2)
        self.setCentralWidget(game)
        self.labelOnePlayer.hide()
        self.labelTwoPlayers.hide()
        self.labelOnlineGame.hide()
        self.labelQuit.hide()

    def mouseOverLabel2P(self, event):
        self.labelTwoPlayers.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabel2P(self, event):
        self.labelTwoPlayers.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")

    def mouseClickedQ(self, event):
        self.labelQuit.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        #self.close()
        process.start()
        processLives.start()
        game = SimMoveDemo(self)
        game.menuSignal.emit(4)
        self.setCentralWidget(game)

        self.labelOnePlayer.hide()
        self.labelTwoPlayers.hide()
        self.labelOnlineGame.hide()
        self.labelQuit.hide()


    def mouseOverLabelQ(self, event):
        self.labelQuit.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabelQ(self, event):
        self.labelQuit.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")

    def mouseClickedOnline(self, event):
        self.labelOnlineGame.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        game = GUI(self)
        game.menuSignal.emit(3)
        self.setCentralWidget(game)

        self.labelOnePlayer.hide()
        self.labelTwoPlayers.hide()
        self.labelOnlineGame.hide()
        self.labelQuit.hide()

    def mouseOverLabelOnline(self, event):
        self.labelOnlineGame.setStyleSheet(
            "QLabel{ background-color:rgba(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabelOnline(self, event):
        self.labelOnlineGame.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    process = Process(target=pointsProcess, args=[queueForCalcs, queueForResults])
    processLives = Process(target=livesProcess, args=[queueCalcLives, queueResLives])

    ex = Menu()
    sys.exit(app.exec_())
