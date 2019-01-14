from PyQt5.QtCore import Qt, QSize, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPalette, QBrush, QImage, QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from key_notifier import KeyNotifier
from Player import Player
from Ball import Ball
from Bonus import *
import time
import random
from settings import *
from multiprocessing import Queue


queueForCalcs = Queue()
queueForResults = Queue()
queueCalcLives = Queue()
queueResLives = Queue()


class SimMoveDemo(QWidget):
    menuSignal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.menuSignal.connect(self.addPlayers)
        self.currentAmp = AMPLITUDE
        self.startingBallSize = MINBALLSIZE*2 + 1
        self.setGeometry(600, 200, WINDOWWIDTH, WINDOWHEIGHT)
        self.players = []
        self.bonuses = []
        self.cupPlayers = []
        self.cupMode = False
        self.finalGame = False
        self.balls = [Ball(self, self.startingBallSize)]
        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()
        self.stopOnStart = True
        self.finishCup = False
        self.playerLen = None
        self.previousBalls = len(self.balls)
        self.currentLevel = 1
        self.currentBall = 0
        self.semiFinalEnd = False
        self.weaponObj = None
        self.weaponObj2 = None
        self.deadPoints = []
        self.finalist1points = 0
        self.finalist2points = 0

    def addPlayers(self, option):
        if option == 1:
            self.players = [Player(self, 'player1', 1)]
        elif option == 2:
            self.players = [Player(self, 'player1', 2), Player(self, 'player2', 2)]
        elif option == 4:
            self.players = [Player(self, 'player1', 2), Player(self, 'player2', 2)]
            self.cupMode = True

        self.__init_ui__()
        self.timer = QBasicTimer()
        self.timer.start(20, self)

    def initPlayersAndBalls(self):
        for player in self.players:
            player.player.setPixmap(player.PixMap)
            player.player.setGeometry(player.PositionX, player.PositionY, player.Width, player.Heigth)
            player.weapon.weapon.setPixmap(player.weapon.PixMap)
            player.weapon.weapon.setGeometry(0, WINDOWHEIGHT-87, WINDOWWIDTH, 0)
            player.livesSignal.connect(self.updateLives)
            player.pointsSignal.connect(self.updatePoints)
        if self.cupMode:
            self.weaponObj = self.players[0].weapon
            self.weaponObj2 = self.players[1].weapon
        for ball in self.balls:
            ball.ball.setPixmap(ball.pixMapScaled)
            ball.ball.setGeometry(ball.x, ball.y, ball.size, ball.size)
        for p in self.players:
            p.show()

    def __init_ui__(self):
        self.initPlayersAndBalls()
        self.setWindowTitle('Bubble Trouble')
        self.stopOnStart = True
        # BACKGROUND
        oImage = QImage(IMAGES_DIR + 'background.png')
        sImage = oImage.scaled(QSize(WINDOWWIDTH, WINDOWHEIGHT))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setFocus()
        self.parent.setPalette(palette)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # elements
        self.livesPic1 = QPixmap(IMAGES_DIR + 'player1.png').scaled(20, 30)
        self.livesPic2 = QPixmap(IMAGES_DIR + 'player2.png').scaled(20, 30)

        verticalPlayerInf = QVBoxLayout()
        self.horizontalBox = QHBoxLayout()

        self.labelLives = []
        for player in self.players:
            self.labelLives.append(self.initPlayerLives(QPixmap(IMAGES_DIR + player.playerId + '.png').scaled(20, 30), player.lifes))

        for label in self.labelLives[0]:
            self.horizontalBox.addWidget(label, 1, Qt.AlignLeft | Qt.AlignTop)

        if len(self.players) > 1:
            self.horizontalBox.addSpacing(WINDOWWIDTH-2*80-75)
            for label in self.labelLives[1]:
                self.horizontalBox.addWidget(label, 1, Qt.AlignRight | Qt.AlignTop)
        else:
            self.horizontalBox.addSpacing(WINDOWWIDTH-150)

        self.initGuiElements(self.horizontalBox, verticalPlayerInf)

        self.setLayout(verticalPlayerInf)

    def initPlayerLives(self, pixMap, currentLives):
        labelLives = []
        for i in range(currentLives):
            labelLives.append(QLabel())
            labelLives[i].setPixmap(pixMap)
        return labelLives

    def updatePlayerPixMapLives(self, pixMap, currentLives, playerUpdated):
        if playerUpdated.playerId == 'player1':
            self.labelLives[0][currentLives].clear()
        elif playerUpdated.playerId == 'player2':
            self.labelLives[1][-currentLives-1].clear()

    def resetPlayerPixMapLives(self, initLives):
        for x in range(2*initLives+1):
            if x != initLives:
                widget = self.horizontalBox.itemAt(x).widget()
            if x < initLives:
                widget.setPixmap(QPixmap(IMAGES_DIR + 'player1.png').scaled(20, 30))
            elif x > initLives:
                widget.setPixmap(QPixmap(IMAGES_DIR + 'player2.png').scaled(20, 30))

    def initGuiElements(self, horizontalBox, verticalPlayerInf):
        self.getReadyLabel = QLabel()
        self.getReadyLabel.setText('Get Ready!')
        self.getReadyLabel.setFont(QFont('Denne Kitten Heels', 30, QFont.ExtraBold))
        self.getReadyLabel.setAlignment(Qt.AlignTop)
        self.getReadyLabel.setFrameStyle(1)
        self.getReadyLabel.setStyleSheet(
            "QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:solid;}")

        self.player11LabelTxt = '1 PLAYER'
        self.player1Tag = QLabel()
        self.player1Tag.setText(self.player11LabelTxt)
        self.player1Tag.setFont(QFont('Denne Kitten Heels', 18, QFont.ExtraBold))
        self.player1Tag.setAlignment(Qt.AlignLeft)
        self.player1Tag.setFrameStyle(33)
        self.player1Tag.setMidLineWidth(1)
        self.player1Tag.setStyleSheet("QLabel{background-color: #CECECE; color:#E20000;}")
        self.player1Tag.setFixedSize(QSize(130, 31))

        self.player2LabelTxt = '2 PLAYER'
        self.player2Tag = QLabel()
        self.player2Tag.setText(self.player2LabelTxt)
        self.player2Tag.setFont(QFont('Denne Kitten Heels', 18, QFont.ExtraBold))
        self.player2Tag.setAlignment(Qt.AlignLeft)
        self.player2Tag.setFrameStyle(33)
        self.player2Tag.setMidLineWidth(1)
        self.player2Tag.setStyleSheet("QLabel{background-color: #CECECE; color:#265EBB;}")
        self.player2Tag.setFixedSize(QSize(130, 31))

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

        self.levelNum = str(self.currentLevel)
        self.levelNumTag = QLabel()
        self.levelNumTag.setText(self.levelNum)
        self.levelNumTag.setFont(QFont('denne kitten heels', 17, QFont.ExtraBold))
        self.levelNumTag.setAlignment(Qt.AlignCenter)
        self.levelNumTag.setStyleSheet("QLabel{background-color: #CECECE; color:#E20000;}")
        self.levelNumTag.setFixedSize(QSize(50, 31))

        horizontalBox.setContentsMargins(20, 0, 20, 0)

        verticalLevel = QVBoxLayout()
        verticalLevel.addWidget(levelTag)
        verticalLevel.addSpacing(-9)
        verticalLevel.addWidget(self.levelNumTag, 0, Qt.AlignCenter)

        horizontalPlayerInf = QHBoxLayout()
        horizontalPlayerInf.addWidget(self.player1Tag)
        horizontalPlayerInf.addWidget(self.player1PointsTag)
        horizontalPlayerInf.addSpacing(90)
        horizontalPlayerInf.addLayout(verticalLevel)
        horizontalPlayerInf.addSpacing(82)
        horizontalPlayerInf.addWidget(self.player2PointsTag)
        horizontalPlayerInf.addWidget(self.player2Tag)

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
            if self.stopOnStart:
                time.sleep(2)
                self.getReadyLabel.close()
            ball.start()
            self.stopOnStart = False
        for bonus in self.bonuses:
            bonus.update()
            bonus.bonus.setPixmap(bonus.pixMapScaled)
            bonus.bonus.setGeometry(bonus.posX, bonus.posY, 30, 30)
            bonus.bonus.show()
        self.checkCollisionWeapon()
        self.checkCollisionPlayer()

    def splitBall(self, size, x, y):
        if size/2 <= MINBALLSIZE:
            if len(self.balls) == 0:
                self.timer.stop()
                time.sleep(1)
                self.loadNextLevel()
        else:

            ball1 = Ball(self, size / 2)
            ball2 = Ball(self, size / 2)

            self.setBallProperties(ball1, x, y, True)
            self.setBallProperties(ball2, x, y, False)

            self.balls.append(ball1)
            self.balls.append(ball2)

            if random.randrange(BONUS_RANGE) == 0:
                bonus_type = random.choice(bonus_types)
                bonus = Bonus(self, bonus_type, x, y)
                bonus.isActive = True
                self.bonuses.append(bonus)

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

                            self.splitBall(size, x, y)
                            player.pointsSignal.emit(50)
                            break  # unisti samo jednu lopticu i izadji (pravi bag ako se izostavi -> unistava
                            # novonastale lopte)

    def checkCollisionPlayer(self):
        for player in self.players:
            for ball in self.balls:
                if player.PositionY <= ball.dy + ball.size-20:
                    if(ball.counter <= player.PositionX and player.PositionX <= ball.counter + ball.size) or \
                     (ball.counter <= player.PositionX + 25 and player.PositionX + 25 <= ball.counter + ball.size) or \
                     (ball.counter <= player.PositionX and ball.counter + ball.size >= player.PositionX + 28) or \
                     (ball.counter >= player.PositionX and ball.counter + ball.size <= player.PositionX + 40):
                        self.timer.stop()
                        ball.ball.hide()
                        self.balls.remove(ball)

                        self.resetLevel()
                        player.livesSignal.emit()
            for bonus in self.bonuses:
                if (player.PositionX + player.Width >= bonus.posX and player.PositionX <= bonus.posX \
                        and bonus.posY + bonus.height >= player.PositionY) or \
                        (player.PositionX <= bonus.posX + bonus.width and player.PositionX >= bonus.posX and bonus.posY + bonus.height >= player.PositionY):

                    if bonus.bonusType == BONUS_COINS:
                        player.pointsSignal.emit(375)
                    elif bonus.bonusType == BONUS_NO_WEAPON:
                        player.weapon.isActive = False
                        player.bonusNoWeapon = True
                    bonus.bonus.hide()
                    self.bonuses.remove(bonus)

    def loadNextLevel(self):
        self.key_notifier.keys.clear()
        self.currentLevel += 1

        nextLevelType = random.choice([0, 1])

        for bonus in self.bonuses:
            bonus.bonus.hide()

        self.bonuses.clear()

        if nextLevelType == 0:
            if self.startingBallSize*2 <= MAXBALLSIZE:
                self.startingBallSize = self.startingBallSize*2
                self.balls.append(Ball(self, self.startingBallSize))
                self.balls[0].ball.setPixmap(self.balls[0].pixMapScaled)
                self.balls[0].ball.setGeometry(self.balls[0].x, self.balls[0].y, self.balls[0].size, self.balls[0].size)
                self.balls[0].ball.show()

                # self.currentAmp =  AMPLITUDE + 46
            else:
                nextLevelType = 1
        if nextLevelType == 1:
            self.previousBalls = self.previousBalls + 1
            temp = self.previousBalls
            for x in range(self.previousBalls):
                self.balls.append(Ball(self, self.startingBallSize))

            for b in self.balls:
                b.ball.setPixmap(b.pixMapScaled)
                if self.currentBall % 2 == 0:
                    b.x = b.x - 35 * temp
                    temp += 1
                    b.counter = b.x
                    b.ball.setGeometry(b.x, b.y, b.size, b.size)
                    b.forward = False
                elif self.currentBall % 2 == 1:
                    b.x = b.x + 35 * temp
                    temp += 1
                    b.counter = b.x
                    b.ball.setGeometry(b.x, b.y, b.size, b.size)
                b.ball.show()
                self.currentBall += 1

        self.stopOnStart = True

        for player in self.players:
            player.PositionX = player.initialPositionX
            player.update(Qt.Key_Minus)
            player.bonusNoWeapon = False
            if player.weapon.isActive:
                player.weapon.isActive = False
                player.weapon.update()

        self.getReadyLabel.setText('Get ready!')
        self.getReadyLabel.show()
        self.getReadyLabel.raise_()
        self.levelNumTag.setText(str(self.currentLevel))
        self.timer.start(20, self)

    def resetLevel(self):
        for ball in self.balls:
            ball.ball.hide()

        self.balls.clear()

        for bonus in self.bonuses:
            bonus.bonus.hide()

        self.bonuses.clear()

        for x in range(self.previousBalls):
            temp = x+2
            self.balls.append(Ball(self, self.startingBallSize))
            self.balls[x].ball.setPixmap(self.balls[x].pixMapScaled)
            if x % 2 == 0:
                if len(self.balls) > 1:
                    self.balls[x].forward = False
                    self.balls[x].x = self.balls[x].x - 35*temp
                self.balls[x].counter = self.balls[x].x
                self.balls[x].ball.setGeometry(self.balls[x].x, self.balls[x].y, self.balls[x].size, self.balls[x].size)
            elif x % 2 == 1:
                self.balls[x].x = self.balls[x].x + 35*temp
                self.balls[x].counter = self.balls[x].x
                self.balls[x].ball.setGeometry(self.balls[x].x, self.balls[x].y, self.balls[x].size, self.balls[x].size)
            self.balls[x].ball.show()

        for player in self.players:
            player.PositionX = player.initialPositionX
            self.key_notifier.keys.clear()
            player.update(Qt.Key_Minus)
            player.bonusNoWeapon = False
            if player.weapon.isActive:
                player.weapon.isActive = False
                player.weapon.update()
        time.sleep(1)
        self.currentAmp = AMPLITUDE
        self.stopOnStart = True

        if not self.semiFinalEnd:
            self.getReadyLabel.setText('Get ready!')
        if not self.finishCup:
            self.timer.start(20, self)
        else:
            # gotov turnir, ispisi rezultate
            self.cupScores()

        self.getReadyLabel.show()
        self.getReadyLabel.raise_()

        self.semiFinalEnd = False

    def getPlayersFromSemifinal1(self, ind):
        points = self.deadPoints[ind].split('_')[0]
        playerName = self.deadPoints[ind].split('_')[1]
        semifinal1 = playerName + ' ' + points + '-' + self.deadPoints[ind+1].split('_')[0] + ' ' + \
                     self.deadPoints[ind+1].split('_')[1]
        return semifinal1

    def cupScores(self):

        # stringovi za ispis rezultata polufinala
        semifinal1 = self.getPlayersFromSemifinal1(0)
        semifinal2 = self.getPlayersFromSemifinal1(2)

        f1points = self.deadPoints[4].split('_')[0]  # finalist 1 points from final
        f1name = self.deadPoints[4].split('_')[1]  # finalist 1 name
        f2points = self.deadPoints[5].split('_')[0]  # finalist 2 points from final
        f2name = self.deadPoints[5].split('_')[1]  # finalist 2 name

        # string za ispis rezultata finala
        final = f1name + ' ' + f1points + '-' + f2points + ' ' + f2name

        # ime pobjednika je u winner-u
        winner = ''

        if int(f1points) > int(f2points):
            winner = f1name
        elif int(f1points) == int(f2points):  # ako imaju isti broj poena u finalu neka pobijedi onaj koji je imao
                                                    # vise u polufinalu, a ako opet imaju isto neka pobijedi domacin
            if int(self.finalist1points) > int(self.finalist2points):  # prvi finalista je imao vise u polufinalu
                winner = f1name
            elif int(self.finalist1points) < int(self.finalist2points):  # drugi finalista je imao vise u polufinalu
                winner = f2name
            else:  # imali su isto poena i u polufinalu
                if int(f1name[0]) < int(f2name[0]):
                    winner = f1name
                else:
                    winner = f2name
        else:
            winner = f2name

        self.getReadyLabel.setText(
            'SF 1: ' + semifinal1 + '\nSF 2: ' + semifinal2 + '\nFINAL: ' + final + '\nWINNER: ' + winner)

    def updateLives(self):
        sender = self.sender()

        livesPic = None
        lives = sender.lifes

        if sender.playerId == 'player1':
            livesPic = self.livesPic1
        elif sender.playerId == 'player2':
            livesPic = self.livesPic2

        queueCalcLives.put(str(lives))
        res = str(queueResLives.get())

        sender.lifes = int(res)

        self.updatePlayerPixMapLives(livesPic, sender.lifes, sender)

        if sender.lifes == 0:
            sender.isDead = True

        if sender.isDead:
            if sender.playerId == 'player1':
                self.deadPoints.append(self.player1PointsTag.text() + '_' + self.player1Tag.text())
            elif sender.playerId == 'player2':
                self.deadPoints.append(self.player2PointsTag.text() + '_' + self.player2Tag.text())
            sender.player.hide()
            self.players.remove(sender)

        if len(self.players) == 0:
            if self.finalGame:
                self.finishCup = True

            p1points = int(self.player1PointsTag.text())
            p2points = int(self.player2PointsTag.text())
            if len(self.cupPlayers) == 0:
                if p1points >= p2points:
                    self.cupPlayers.append('1 player,' + str(p1points))
                else:
                    self.cupPlayers.append('2 player,' + str(p2points))
            else:
                if p1points >= p2points:
                    self.cupPlayers.append('3 player,' + str(p1points))
                else:
                    self.cupPlayers.append('4 player,' + str(p2points))
            self.gameOver()

    def updatePoints(self, num):
        sender = self.sender()

        playerLabel = None
        previous = None

        if sender.playerId == 'player1':
            previous = self.player1PointsTag.text()
            playerLabel = self.player1PointsTag
        elif sender.playerId == 'player2':
            previous = self.player2PointsTag.text()
            playerLabel = self.player2PointsTag

        queueForCalcs.put(sender.playerId+','+ str(previous)+','+ str(num))
        points = str(queueForResults.get())

        playerLabel.setText(points)

    def gameOver(self):
        if not self.cupMode:
            self.getReadyLabel.setText("Game over")
            self.getReadyLabel.show()
            self.getReadyLabel.raise_()

        self.timer.stop()

        if self.cupMode:
            self.playerWon = self.cupPlayers[len(self.cupPlayers) - 1]
            self.getReadyLabel.setText(self.playerWon.split(',')[0].upper() + " WON!")
            self.cupModeLogic()

    def cupModeLogic(self):
        self.players = [Player(self, 'player1', 2), Player(self, 'player2', 2)]

        self.initStartingLevel()
        self.initCupPlayers()

        self.resetPlayerPixMapLives(self.players[0].lifes)

        if len(self.cupPlayers) == 1:  # pocelo drugo polufinale
            self.getReadyLabel.setText(self.playerWon.split(',')[0].upper() + " WON!")

            self.player1Tag.setText('3 PLAYER')
            self.player2Tag.setText('4 PLAYER')
        else:  # pocelo finale
            finalist1 = self.cupPlayers[0].split(',')[0]
            self.finalist1points = self.cupPlayers[0].split(',')[1]
            finalist2 = self.cupPlayers[1].split(',')[0]
            self.finalist2points = self.cupPlayers[1].split(',')[1]

            self.player1Tag.setText(finalist1.upper())
            self.player2Tag.setText(finalist2.upper())

            self.finalGame = True
        self.resetLevel()

    def initStartingLevel(self):  # vrati poene na 0, loptu na inicijalnu, level na 1
        self.player1PointsTag.setText('0')
        self.player2PointsTag.setText('0')
        self.semiFinalEnd = True
        self.currentLevel = 1
        self.levelNumTag.setText(str(self.currentLevel))
        self.previousBalls = 1
        self.currentAmp = AMPLITUDE
        self.startingBallSize = MINBALLSIZE * 2 + 1
        self.semiFinalEnd = True

    def initCupPlayers(self):
        self.players[0].weapon.weapon = self.weaponObj.weapon
        self.players[1].weapon.weapon = self.weaponObj2.weapon

        for p in self.players:
            p.player.setPixmap(p.PixMap)
            p.weapon.weapon.show()
            p.livesSignal.connect(self.updateLives)
            p.pointsSignal.connect(self.updatePoints)

            p.player.show()
