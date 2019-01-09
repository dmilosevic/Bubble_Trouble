from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QImage, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from settings import *


class Menu(QWidget):
    showForm2Signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setGeometry(600, 200, WINDOWWIDTH, WINDOWHEIGHT)

        self.isActive = True
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

        self.labelQuit = self.initLabel("QUIT")

        self.labelOnePlayer.setGeometry(175, 235, 185, 35)
        self.labelTwoPlayers.setGeometry(165, 295, 185, 35)
        self.labelQuit.setGeometry(215, 350, 185, 35)

        self.labelOnePlayer.mousePressEvent = self.mouseClicked1P
        self.labelOnePlayer.enterEvent = self.mouseOverLabel1P
        self.labelOnePlayer.leaveEvent = self.mouseLeftLabel1P

        self.labelTwoPlayers.mousePressEvent = self.mouseClicked2P
        self.labelTwoPlayers.enterEvent = self.mouseOverLabel2P
        self.labelTwoPlayers.leaveEvent = self.mouseLeftLabel2P

        self.labelQuit.mousePressEvent = self.mouseClickedQ
        self.labelQuit.enterEvent = self.mouseOverLabelQ
        self.labelQuit.leaveEvent = self.mouseLeftLabelQ

        self.setLayout(self.layout)

        self.show()

    def initLabel(self, text):
        label = QLabel(text, self)
        label.setFont(QFont('Denne Kitten Heels', 25, QFont.ExtraBold))
        label.setAlignment(Qt.AlignTop)
        label.setFrameStyle(1)
        label.setStyleSheet(
            "QLabel{ background-color:rgb(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")
        label.setFixedSize(QSize(185, 35))
        return label

    def mouseClicked1P(self, event):
        self.labelOnePlayer.setStyleSheet(
            "QLabel{ background-color:rgb(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        self.isActive = False
        self.showForm2Signal.emit()

    def mouseOverLabel1P(self, event):
        self.labelOnePlayer.setStyleSheet(
            "QLabel{ background-color:rgb(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabel1P(self, event):
        self.labelOnePlayer.setStyleSheet(
            "QLabel{ background-color:rgb(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")

    def mouseClicked2P(self, event):
        self.labelTwoPlayers.setStyleSheet(
            "QLabel{ background-color:rgb(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        self.isActive = False

    def mouseOverLabel2P(self, event):
        self.labelTwoPlayers.setStyleSheet(
            "QLabel{ background-color:rgb(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabel2P(self, event):
        self.labelTwoPlayers.setStyleSheet(
            "QLabel{ background-color:rgb(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")

    def mouseClickedQ(self, event):
        self.labelQuit.setStyleSheet(
            "QLabel{ background-color:rgb(66, 134, 244, 0.4) ;color:#4286f4 ;border-width:1px; border-style:none;}")
        self.isActive = False

    def mouseOverLabelQ(self, event):
        self.labelQuit.setStyleSheet(
            "QLabel{ background-color:rgb(66, 134, 244, 0.4) ;color:#ffffff ;border-width:1px; border-style:none;}")

    def mouseLeftLabelQ(self, event):
        self.labelQuit.setStyleSheet(
            "QLabel{ background-color:rgb(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:none;}")
