from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap
from settings import *
from math import *


class Ball(QWidget):
    def __init__(self, parent, size):

        super().__init__(parent)

        self.size = size
        self.ball = QLabel(parent)
        self.pixMap = QPixmap(IMAGES_DIR + 'bubble.png')
        self.pixMapScaled = self.pixMap.scaled(size, size)
        self.counter = 400
        self.forward = True
        self.sinus = True
        self.hit = False
        self.splited = False
        self.splitedLeft = False
        self.splitedRight = False
        self.splitedCounter = None
        self.y = WINDOWHEIGHT - 450
        self.x = WINDOWWIDTH / 2 - size / 2
        self.dy = 0
        self.currentAmplitude = AMPLITUDE - (AMPLITUDE-size*4)

    def start(self):
        if self.forward:
            if self.counter + BALL_STEP >= 796:  # udario u desni zid
                self.hit = True
                self.forward = False
                self.counter = self.counter - BALL_STEP
                if self.splitedLeft or self.splitedRight:
                    self.splitedCounter = self.splitedCounter + BALL_STEP
            else:
                self.hit = False
                if self.splitedLeft or self.splitedRight:
                    self.splitedCounter = self.splitedCounter - BALL_STEP
                self.counter = self.counter + BALL_STEP  # just going forward
        else:
            if self.counter - BALL_STEP <= 42:  # udario u lijevi zid
                self.hit = True
                self.forward = True
                self.counter = self.counter + BALL_STEP
                if self.splitedLeft or self.splitedRight:
                    self.splitedCounter = self.splitedCounter - BALL_STEP
            else:
                self.hit = False
                self.counter = self.counter - BALL_STEP  # just going backwards
                if self.splitedLeft or self.splitedRight:
                    self.splitedCounter = self.splitedCounter + BALL_STEP

        self.calculate_dy()
        self.ball.setGeometry(self.counter, self.dy, self.size, self.size)

    def calculate_dy(self):
        if self.hit:
            self.sinus = not self.sinus
      
        if self.sinus and not self.splited:
            self.dy = -abs(AMPLITUDE * sin(3*self.counter/1.6/100)) + 400 - self.size
        elif not self.sinus and not self.splited:
            self.dy = -abs(AMPLITUDE * cos(3*self.counter/1.6/100)) + 400 - self.size
        if self.sinus and self.splitedLeft:
            self.dy = -abs(self.currentAmplitude * cos(3*self.splitedCounter/1.6/100)) + 400 - self.size
        elif not self.sinus and self.splitedLeft:
            self.dy = -abs(self.currentAmplitude * sin(3 * self.splitedCounter / 1.6 / 100)) + 400 - self.size
        if self.sinus and self.splitedRight:
            self.dy = -abs(self.currentAmplitude * sin(3*self.splitedCounter/1.6/100)) + 400 - self.size
            #self.currentAmplitude -= 50
        elif not self.sinus and self.splitedRight:
            self.dy = -abs(self.currentAmplitude * cos(3 * self.splitedCounter / 1.6 / 100)) + 400 - self.size
            #self.currentAmplitude -= 50