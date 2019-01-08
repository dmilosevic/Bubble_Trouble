import sys

from PyQt5.QtCore import Qt, QSize, QBasicTimer,QRect, QRectF
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage, QPainter, QPen, QFont,QPainterPath,QRegion
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QGroupBox
from settings import *
from key_notifier import KeyNotifier
from Player import Player
from Ball import Ball
import time
from settings import *
import os

class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()

        self.currentAmp = AMPLITUDE
        self.startingBallSize = 60
        self.setGeometry(600, 200, WINDOWWIDTH, WINDOWHEIGHT)
        self.players = [Player(self, 'player2'), Player(self, 'player1')]
        self.balls = [Ball(self, self.startingBallSize)]
        self.__init_ui__()
        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()
        self.timer = QBasicTimer()
        self.timer.start(20, self)
        self.stopOnStart = True

    def initPlayersAndBalls(self):
        for player in self.players:
            player.player.setPixmap(player.PixMap)
            player.player.setGeometry(player.PositionX, player.PositionY, player.Width, player.Heigth)
            player.weapon.weapon.setPixmap(player.weapon.PixMap)
            player.weapon.weapon.setGeometry(0, WINDOWHEIGHT-87, WINDOWWIDTH, 0)
            player.livesSignal.connect(self.updateLives)
            player.pointsSignal.connect(self.updatePoints)
        for ball in self.balls:
            ball.ball.setPixmap(ball.pixMapScaled)
            ball.ball.setGeometry(ball.x, ball.y, ball.size, ball.size)
        self.players[0].show()
        self.players[1].show()
    def __init_ui__(self):
        self.initPlayersAndBalls()
        self.setWindowTitle('Bubble Trouble')
        self.stopOnStart = True
        #BACKGROUND
        oImage = QImage(IMAGES_DIR + 'background.png')
        sImage = oImage.scaled(QSize(WINDOWWIDTH, WINDOWHEIGHT))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)

        #elements
        self.livesPic1 = QPixmap(IMAGES_DIR + 'player1.png').scaled(20, 30)
        self.livesPic2 = QPixmap(IMAGES_DIR + 'player2.png').scaled(20, 30)

        self.labelLivesP1 = self.initPlayerLives(self.livesPic1, self.players[0].lifes)
        self.labelLivesP2 = self.initPlayerLives(self.livesPic2, self.players[1].lifes)
        verticalPlayerInf = QVBoxLayout()
        horizontalBox = QHBoxLayout()

        for label in self.labelLivesP1:
            horizontalBox.addWidget(label,1,Qt.AlignLeft | Qt.AlignTop)
        horizontalBox.addSpacing(WINDOWWIDTH-2*80-75)
        for label in self.labelLivesP2:
            horizontalBox.addWidget(label,1,Qt.AlignRight | Qt.AlignTop)

        self.initGuiElements(horizontalBox, verticalPlayerInf)

        #self.players[0].weapon.weapon.show()
        #self.players[1].weapon.weapon.show()

        self.setLayout(verticalPlayerInf)
        self.show()

    def initPlayerLives(self, pixMap, currentLives):
        labelLives = []
        for i in range(currentLives):
            labelLives.append(QLabel())
            labelLives[i].setPixmap(pixMap)
        return labelLives

    def updatePlayerPixMapLives(self,pixMap, currentLives, playerUpdated):
        if playerUpdated.playerId == 'player1':
            self.labelLivesP1[currentLives].clear()
        elif playerUpdated.playerId == 'player2':
            self.labelLivesP2[-currentLives-1].clear()

    def initGuiElements(self, horizontalBox, verticalPlayerInf):
        self.getReadyLabel = QLabel()
        self.getReadyLabel.setText('Get Ready!')
        self.getReadyLabel.setFont(QFont('Denne Kitten Heels', 30, QFont.ExtraBold))
        self.getReadyLabel.setAlignment(Qt.AlignTop)
        self.getReadyLabel.setFrameStyle(1)
        self.getReadyLabel.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:solid;}")

        player11LabelTxt = '1 PLAYER'
        player1Tag = QLabel()
        player1Tag.setText(player11LabelTxt)
        player1Tag.setFont(QFont('Denne Kitten Heels', 18, QFont.ExtraBold))
        player1Tag.setAlignment(Qt.AlignLeft)
        player1Tag.setFrameStyle(33)
        player1Tag.setMidLineWidth(1)
        player1Tag.setStyleSheet("QLabel{background-color: #CECECE; color:#E20000;}")
        player1Tag.setFixedSize(QSize(130, 31))

        player2LabelTxt = '2 PLAYER'
        player2Tag = QLabel()
        player2Tag.setText(player2LabelTxt)
        player2Tag.setFont(QFont('Denne Kitten Heels', 18, QFont.ExtraBold))
        player2Tag.setAlignment(Qt.AlignLeft)
        player2Tag.setFrameStyle(33)
        player2Tag.setMidLineWidth(1)
        player2Tag.setStyleSheet("QLabel{background-color: #CECECE; color:#265EBB;}")
        player2Tag.setFixedSize(QSize(130, 31))

        player1Points = '0'
        self.player1PointsTag = QLabel()
        self.player1PointsTag.setText(player1Points)
        self.player1PointsTag.setFont(QFont('kristen itc', 17, QFont.ExtraBold))
        self.player1PointsTag.setAlignment(Qt.AlignRight)
        self.player1PointsTag.setFrameStyle(33)
        self.player1PointsTag.setMidLineWidth(1)
        self.player1PointsTag.setStyleSheet("QLabel{background-color: #CECECE; color:#676769;}")
        self.player1PointsTag.setFixedSize(QSize(100, 31))

        player2Points = '0'
        self.player2PointsTag = QLabel()
        self.player2PointsTag.setText(player2Points)
        self.player2PointsTag.setFont(QFont('kristen itc', 17, QFont.ExtraBold))
        self.player2PointsTag.setAlignment(Qt.AlignRight)
        self.player2PointsTag.setFrameStyle(33)
        self.player2PointsTag.setMidLineWidth(1)
        self.player2PointsTag.setStyleSheet("QLabel{background-color: #CECECE; color:#676769;}")
        self.player2PointsTag.setFixedSize(QSize(100, 31))

        levelText = 'Level'
        levelTag = QLabel()
        levelTag.setText(levelText)
        levelTag.setFont(QFont('denne kitten heels', 17, QFont.ExtraBold))
        levelTag.setAlignment(Qt.AlignCenter)
        levelTag.setFrameStyle(33)
        levelTag.setMidLineWidth(1)
        levelTag.setStyleSheet("QLabel{background-color: #CECECE; color:#C7820D;}")
        levelTag.setFixedSize(QSize(100, 31))

        levelNum = '1'
        levelNumTag = QLabel()
        levelNumTag.setText(levelNum)
        levelNumTag.setFont(QFont('denne kitten heels', 17, QFont.ExtraBold))
        levelNumTag.setAlignment(Qt.AlignCenter)
        levelNumTag.setStyleSheet("QLabel{background-color: #CECECE; color:#E20000;}")
        levelNumTag.setFixedSize(QSize(50, 31))

        horizontalBox.setContentsMargins(20, 0, 20, 0)

        verticalLevel = QVBoxLayout()
        verticalLevel.addWidget(levelTag)
        verticalLevel.addSpacing(-9)
        verticalLevel.addWidget(levelNumTag,0,Qt.AlignCenter)

        horizontalPlayerInf = QHBoxLayout()
        horizontalPlayerInf.addWidget(player1Tag)
        horizontalPlayerInf.addWidget(self.player1PointsTag)
        horizontalPlayerInf.addSpacing(90)
        horizontalPlayerInf.addLayout(verticalLevel)
        horizontalPlayerInf.addSpacing(82)
        horizontalPlayerInf.addWidget(self.player2PointsTag)
        horizontalPlayerInf.addWidget(player2Tag)

        horizontalPlayerInf.setAlignment(Qt.AlignBottom)
        horizontalPlayerInf.setContentsMargins(10, 0, 10, 0)
        verticalPlayerInf.addLayout(horizontalBox)
        verticalPlayerInf.addWidget(self.getReadyLabel, 1, Qt.AlignCenter | Qt.AlignTop)
        verticalPlayerInf.addLayout(horizontalPlayerInf)


    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())
        if not event.isAutoRepeat():
            for player in self.players:
                player.drawPlayer('normal')

    def __update_position__(self, key):
        for player in self.players:
            player.update(key)

    def closeEvent(self, event):
        self.key_notifier.die()

    def timerEvent(self, event):
        for ball in self.balls:
            if(self.stopOnStart):
                time.sleep(2)
                self.getReadyLabel.close()
            ball.start()
            self.stopOnStart = False
        self.checkCollisionWeapon()
        self.checkCollisionPlayer()

    def splitBall(self, size, x, y):
        if size/2 <= MINBALLSIZE:
            if len(self.balls) == 0:
                print('kraj nivoa')
        else:

            ball1 = Ball(self, size / 2)
            ball2 = Ball(self, size / 2)

            self.setBallProperties(ball1, x, y, True)
            self.setBallProperties(ball2, x, y, False)

            self.balls.append(ball1)
            self.balls.append(ball2)

            ball1.splitedLeft = True
            ball2.splitedRight = True
            ball1.splitedCounter = 42
            ball2.splitedCounter = 42
            ball1.y = ball1.dy
            ball2.y = ball2.dy
            ball1.ball.show()
            ball2.ball.show()

    def setBallProperties(self, ball, x, y, isForward):
        ball.counter = x
        ball.dy = y
        ball.forward = isForward
        ball.ball.setPixmap(ball.pixMapScaled)
        ball.ball.setGeometry(ball.counter, ball.dy, ball.size, ball.size)

    def checkCollisionWeapon(self):
        for player in self.players:
            if player.weapon.isActive:
                for ball in self.balls:
                    if ball.counter <= player.weapon.posX and ball.counter + ball.size >= player.weapon.posX:
                        if ball.dy + ball.size >= player.weapon.posY:
                            player.weapon.isActive = False
                            size = ball.size
                            x = ball.counter
                            y = ball.dy
                            self.balls.remove(ball)
                            ball.ball.hide()
                            del ball
                            
                            #ball.ball.setGeometry(0,0,0,0)
                            #ball = None
                            self.splitBall(size, x, y)
                            player.pointsSignal.emit(50)
                            break #unisti samo jednu lopticu i izadji (pravi bag ako se izostavi -> unistava novonastale lopte)

    def checkCollisionPlayer(self):
        for player in self.players:
            for ball in self.balls:
                if player.PositionY <= ball.dy + ball.size-20:
                    if(ball.counter <= player.PositionX and player.PositionX <= ball.counter + ball.size) or \
                        (ball.counter <= player.PositionX + 25 and player.PositionX + 25 <= ball.counter + ball.size) or \
                        (ball.counter <= player.PositionX and ball.counter + ball.size >= player.PositionX + 28) or \
                        (ball.counter >= player.PositionX and ball.counter + ball.size <= player.PositionX + 40):
                        # print('udario')
                        self.timer.stop()
                        ball.ball.hide()
                        self.balls.remove(ball)

                        time.sleep(1)
                        self.resetLevel()
                        player.livesSignal.emit(1)

    def resetLevel(self):
        for ball in self.balls:
            ball.ball.hide()

        self.balls.clear()

        self.balls.append(Ball(self, self.startingBallSize))
        self.balls[0].ball.setPixmap(self.balls[0].pixMapScaled)
        self.balls[0].ball.setGeometry(self.balls[0].x, self.balls[0].y, self.balls[0].size, self.balls[0].size)
        self.balls[0].ball.show()

        for player in self.players:
            player.PositionX = player.initialPositionX
            player.update(Qt.Key_Minus)
            if player.weapon.isActive == True:
                player.weapon.isActive = False
                player.weapon.update()
        self.currentAmp = AMPLITUDE
        self.stopOnStart = True
        self.getReadyLabel.show()
        self.getReadyLabel.raise_()
        self.timer.start(20, self)

    def updateLives(self, num):
        sender = self.sender()
        if sender.playerId == 'player1':
            sender.updateLives(num)
            self.updatePlayerPixMapLives(self.livesPic1, sender.lifes, sender)
        elif sender.playerId == 'player2':
            sender.updateLives(num)
            self.updatePlayerPixMapLives(self.livesPic2, sender.lifes, sender)

        if sender.isDead:
            sender.player.hide()
            self.players.remove(sender)

        if len(self.players) == 0:
            self.gameOver()

    def updatePoints(self, num):
        sender = self.sender()
        if sender.playerId == 'player1':
            previous = self.player1PointsTag.text()
            updatedPoints = int(previous) + 50
            self.player1PointsTag.setText(str(updatedPoints))
        elif sender.playerId == 'player2':
            previous = self.player2PointsTag.text()
            updatedPoints = int(previous) + 50
            self.player2PointsTag.setText(str(updatedPoints))

    def gameOver(self):
        self.getReadyLabel.setText("Game over")
        self.getReadyLabel.show()
        self.getReadyLabel.raise_()
        self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())