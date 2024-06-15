from Common.Settings import *


class Bonus:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.isActive = False
        self.heigth = 30
        self.width = 30



    def update(self):
        if self.isActive:
            if self.y + BONUS_STEP <= 395 - self.heigth:
                self.y += BONUS_STEP
            else:
                self.isActive = False

    def toString(self):
        return str(self.type) + ',' + str(self.x) + ',' + str(self.y)