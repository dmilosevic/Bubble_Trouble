from Common.Settings import *

class Player:
    def __init__(self, Id, posX):
        self.positionX = posX
        self.Id = Id
        self.positionY = PLAYER_HEIGTH

        self.bonusNoWeapon = False
        self.counterBonus = 0

        self.isAlive = True

        self.Width = 50
        self.lives = 1
        self.points = 0
