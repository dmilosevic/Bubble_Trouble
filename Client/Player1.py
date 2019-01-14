from PyQt5.QtWidgets import *
from Common.Settings import *
from PyQt5.QtGui import *
from Client import *

class Player(QWidget):
    def __init__(self,parent, playerId):
        super().__init__(parent)

        self.Normal = True
        self.Left = False
        self.Right = False

        self.playerId = playerId

        self.playerImg_normal = IMAGES_DIR + self.playerId + '.png'
        self.playerImg_left = IMAGES_DIR + self.playerId + '_left.png'
        self.playerImg_right = IMAGES_DIR + self.playerId + '_right.png'

        self.player = QLabel(parent)
        self.wimage = IMAGES_DIR + 'weapon.png'
        self.wPixMap = QPixmap(self.wimage)
        self.weapon = QLabel(parent)
        self.weapon.setPixmap(self.wPixMap)
        self.weapon.hide()
        self.PixMap = QPixmap(self.playerImg_normal)


    def drawPlayer(self, orientation):
        if orientation == 'normal':
            self.Normal = True
            self.Left = False
            self.Right = False
            self.PixMap = QPixmap(self.playerImg_normal)

        elif orientation == 'left':
            self.Normal = False
            self.Left = True
            self.Right = False
            self.PixMap = QPixmap(self.playerImg_left)
        elif orientation == 'right':
            self.Normal = False
            self.Left = False
            self.Right = True
            self.PixMap = QPixmap(self.playerImg_right)

        self.player.setPixmap(self.PixMap)

