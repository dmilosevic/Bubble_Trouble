from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from settings import *


class Weapon(QWidget):
    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent
        self.image = IMAGES_DIR + 'weapon.png'
        self.isActive = False
        self.weapon = QLabel(parent)
        self.PixMap = QPixmap(self.image)
        self.weapon.setPixmap(self.PixMap)
        self.posY = self.parent.PositionY
        self.posX = 0
        self.taken = False

    def update(self):

        if self.isActive:
            if not self.taken:
                self.posX = self.parent.PositionX + 14
                self.taken = True
            if self.posY <= 0:
                self.isActive = False
                self.taken = False
                self.posY = self.parent.PositionY
                self.weapon.setGeometry(0, 0, 0, 0)
            else:
                self.weapon.setGeometry(self.posX, self.posY, 8, WINDOWHEIGHT)
                self.posY -= WEAPON_SPEED
        else:
            self.weapon.setGeometry(0, 0, 0, 0)
            self.posY = self.parent.PositionY
            self.taken =  False

