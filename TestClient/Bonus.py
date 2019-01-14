from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from settings import *

BONUS_COINS = 'Coin.png'
BONUS_NO_WEAPON = 'noweapon.png'

bonus_types = [BONUS_COINS, BONUS_NO_WEAPON]


class Bonus(QWidget):
    def __init__(self, parent, bonusImg, x, y):
        super().__init__(parent)

        self.bonusType = bonusImg
        self.bonus = QLabel(parent)
        self.pixMap = QPixmap(IMAGES_DIR + self.bonusType)
        if self.bonusType == BONUS_COINS:
            self.width = 30
            self.height = 30
        else:
            self.width = 20
            self.height = 30
        self.pixMapScaled = self.pixMap.scaled(self.width, self.height)
        self.posX = x
        self.posY = y
        self.isActive = False

    def update(self):
        if self.isActive:
            if self.posY + BONUS_STEP <= 395 - self.height:
                self.posY += BONUS_STEP
            else:
                self.isActive = False
