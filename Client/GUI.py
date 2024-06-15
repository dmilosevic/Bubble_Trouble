from PyQt5.QtCore import QSize, Qt, QBasicTimer, pyqtSignal
from .key_notifier1 import KeyNotifier
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Player1 import *
from Client import *


class GUI(QWidget):
    menuSignal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.players = [Player(self, 'player1'), Player(self, 'player2')]
        self.menuSignal.connect(self.initPlayers)
        # self.currentAmp = AMPLITUDE
        # self.startingBallSize = 180
        self.setGeometry(600, 200, WINDOWWIDTH, WINDOWHEIGHT)
        self.ballLabels = []
        self.bonusesLabels = []
        self.ballPixMap = QPixmap(IMAGES_DIR + 'bubble.png')
        print('bubble :', IMAGES_DIR +'bubble.png')
        self.bonusPixMap1 = QPixmap(IMAGES_DIR + 'Coin.png').scaled(30, 30)
        self.bonusPixMap2 = QPixmap(IMAGES_DIR + 'noweapon.png')
        # self.players = []
        # self.bonuses = []
        # self.balls = [Ball(self, self.startingBallSize)]

        # self.labelPlayer1 = QLabel()
        # self.pixM

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()
        # self.onlineMode = False
        #
        # self.stopOnStart = True
        # self.playerLen = None

        self.timer = QBasicTimer()
        self.timer.start(20, self)

        self.currentLevel = 1

        self.livesPic1 = QPixmap(IMAGES_DIR + 'player1.png').scaled(20, 30)
        self.livesPic2 = QPixmap(IMAGES_DIR + 'player2.png').scaled(20, 30)

        self.verticalPlayerInf = QVBoxLayout()
        self.horizontalBox = QHBoxLayout()

        self.__init_ui__()

        self.client = Client()
        self.client.runThreads()

    def __init_ui__(self):
        # self.initPlayersAndBalls()
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
        self.labelLives = []
        # self.labelLivesP1 = self.initPlayerLives(self.livesPic1, self.players[0].lifes)
        # self.labelLivesP2 = self.initPlayerLives(self.livesPic2, self.players[1].lifes)
        self.labelLives.append(self.drawPlayerLives(self.livesPic1, 3))
        self.labelLives.append(self.drawPlayerLives(self.livesPic2, 3))
        self.initGuiElements()

        self.setLayout(self.verticalPlayerInf)
        self.setLabelLives()

    def drawPlayerLives(self, pixMap, currentLives):
        labelLives = []
        for i in range(currentLives):
            labelLives.append(QLabel())
            labelLives[i].setPixmap(pixMap)
        return labelLives

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())
        if not event.isAutoRepeat():
            for player in self.players:
                player.drawPlayer('normal')

    def __update_position__(self, key):
        # for player in self.players:
        self.client.sendThread.senderSignal.emit(str(key)) # prosledi serveru key

    def initPlayers(self, num):
        if num == 1:
            self.players = [Player(self, 'player1')]
        elif num == 2:
            self.players = [Player(self, 'player1'), Player(self, 'player2')]
        elif num == 3:
            self.players = [Player(self, 'player1'), Player(self, 'player2')]

        self.client.sendThread.senderSignal.emit(str(num))
                                                                                   #bonus     #lopta   #lopta
    def update(self, responseMsg):      # p1X,p2X,orient1,orient2,w1X,w1Y,w2X,w2Y@bType,x,y@#x,y,size#x,y,size#|
        print(responseMsg)
        if responseMsg is not None:
            for b in self.ballLabels:
                b.hide()
            self.ballLabels.clear()
            for b in self.bonusesLabels:
                b.hide()
            self.bonusesLabels.clear()

            respArray = responseMsg.split('|')
            for t in respArray:
                if t != '':
                    players = t.split('#')[0]
                    bonuses = players.split('@')
                    balls = t.split('#')
                    players = players.split('@')[0]

                    self.updateBonuses(bonuses[1:])
                    self.updateBalls(balls[1:])
                    self.updatePlayers(players)


    def updateBalls(self, balls):
        if balls == '':
            return
        for b in balls:
            if b != '':
                x = int(b.split(',')[0])
                y = float(b.split(',')[1])
                size = int(b.split(',')[2])
                lab = QLabel(self)
                pixMapScaled = self.ballPixMap.scaled(size, size)
                lab.setPixmap(pixMapScaled)
                lab.setGeometry(x, y, size, size)
                self.ballLabels.append(lab)
                lab.show()

    def updateBonuses(self, bonuses):
        if bonuses == '':
            print('prazni bonusi')
            return
        for bonus in bonuses:
            if bonus != '':
                print('ima bonus')
                type = int(bonus.split(',')[0])
                x = int(bonus.split(',')[1])
                y = float(bonus.split(',')[2])
                lab = QLabel(self)
                pixMapScaled = ''
                if type == BONUS_COINS:
                    pixMapScaled = self.bonusPixMap1
                elif type==BONUS_NO_WEAPON:
                    pixMapScaled = self.bonusPixMap2

                lab.setPixmap(pixMapScaled)
                lab.setGeometry(x, y, 30, 30)
                self.bonusesLabels.append(lab)
                lab.show()

    def updatePlayers(self, players):
        PositionXP1 = players.split(',')[0]
        PositionXP2 = players.split(',')[1]
        orientation1 = players.split(',')[2]
        orientation2 = players.split(',')[3]
        weapon1X = players.split(',')[4]
        weapon1Y = players.split(',')[5]
        weapon2X = players.split(',')[6]
        weapon2Y = players.split(',')[7]
        pointsP1 = players.split(',')[8]
        pointsP2 = players.split(',')[9]
        livesP1 = int(players.split(',')[10])
        livesP2 = int(players.split(',')[11])
        level = players.split(',')[12]



        for lab in self.labelLives:
            for pic in lab:
                pic.clear()
        # self.labelLives.clear()

        self.levelNumTag.setText(level)

        for player in self.players:
            if player.playerId == 'player1':
                if livesP1 <= 0:
                    try:
                        player.player.hide()
                        player.weapon.hide()
                        continue
                    except:
                        continue
                player.drawPlayer(orientation1)
                if int(weapon1Y) == PLAYER_HEIGTH:
                    player.weapon.setGeometry(0, 0, 0, 0)
                else:
                    player.weapon.setGeometry(int(weapon1X) + 13, int(weapon1Y), 8, WINDOWHEIGHT)
                    player.weapon.show()
                player.player.setGeometry(int(PositionXP1), PLAYER_HEIGTH, PLAYER_SIZE, PLAYER_SIZE)
                player.player.show()
                player.player.raise_()
                for i in range(livesP1):
                    self.labelLives[0][i].setPixmap(self.livesPic1)
                self.player1PointsTag.setText(pointsP1)
            if player.playerId == 'player2':
                if livesP2 <= 0:
                    try:
                        player.player.hide()
                        player.weapon.hide()
                        continue
                    except:
                        continue
                player.drawPlayer(orientation2)
                if int(weapon2Y) == PLAYER_HEIGTH:
                    player.weapon.setGeometry(0, 0, 0, 0)
                else:
                    player.weapon.setGeometry(int(weapon2X) + 13, int(weapon2Y), 8, WINDOWHEIGHT)
                    player.weapon.show()
                player.player.setGeometry(int(PositionXP2), PLAYER_HEIGTH, PLAYER_SIZE, PLAYER_SIZE)
                player.player.show()
                player.player.raise_()
                for i in range(livesP2):
                    self.labelLives[1][-(i+1)].setPixmap(self.livesPic2)
                self.player2PointsTag.setText(pointsP2)

        if int(PositionXP1) == -100 and int(PositionXP2) == -100:
            self.getReadyLabel.setText('Game over')
            return

    def setLabelLives(self):
        for label in self.labelLives[0]:
            self.horizontalBox.addWidget(label, 1, Qt.AlignLeft | Qt.AlignTop)

        if len(self.players) > 1:
            self.horizontalBox.addSpacing(WINDOWWIDTH-2*80-75)
            for label in self.labelLives[1]:
                self.horizontalBox.addWidget(label, 1, Qt.AlignRight | Qt.AlignTop)
        else:
            self.horizontalBox.addSpacing(WINDOWWIDTH-150)

    def timerEvent(self, event):
        if not queueClient.empty():
            returnMsg = str(queueClient.get())
            self.update(returnMsg)

    def initGuiElements(self):
        self.getReadyLabel = QLabel()
        self.getReadyLabel.setText('Get Ready!')
        self.getReadyLabel.setFont(QFont('Denne Kitten Heels', 30, QFont.ExtraBold))
        self.getReadyLabel.setAlignment(Qt.AlignTop)
        self.getReadyLabel.setFrameStyle(1)
        self.getReadyLabel.setStyleSheet("QLabel{ background-color:rgba(81, 109, 131, 0.4) ;color:#D9C91B ;border-width:1px; border-style:solid;}")

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

        self.horizontalBox.setContentsMargins(20, 0, 20, 0)

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
        self.verticalPlayerInf.addLayout(self.horizontalBox)
        self.verticalPlayerInf.addWidget(self.getReadyLabel, 1, Qt.AlignCenter | Qt.AlignTop)
        self.verticalPlayerInf.addLayout(horizontalPlayerInf)