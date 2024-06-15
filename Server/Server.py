from Common.ThreadRcv import *
from Common.ThreadSend import *
from Common.Settings import *
from PyQt5.QtCore import QObject,Qt, QMutex, pyqtSignal, pyqtSlot
from multiprocessing import Queue
import socket
from Ball import *
import time
from Player import *
from Bonus import *
import random
import math

queue = Queue()
queueResponse = Queue()
balls = [Ball(MINBALLSIZE * 2 + 1)]
players = [Player('player1', 50), Player('player2', 700)]
bonuses = []

class Server(QObject):
    Weapon1 = False
    Weapon2 = False
    w1X = 50
    w2X = 700
    w1Y = PLAYER_HEIGTH
    w2Y = PLAYER_HEIGTH

    player1X = 50
    player2X = 700
    #receivedMsg = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.numberOfClients = 0
        self.HOST = '192.168.0.18'#'192.168.0.67'
        self.PORT = 50000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(2)
        print("Waiting for connections...")
        self.threads = []
        self.receivedMsg = None
        self.clientsConnected = []
        self.sendThreads = []
        self.rvcThreads = []
        self.ballsThread = QThread()
        self.moveToThread(self.ballsThread)
        # Connect Thread started signal to Worker operational slot method
        self.ballsThread.started.connect(self.update)

        self.previousBalls = len(balls)
        self.startingBallSize = MINBALLSIZE * 2 + 1
        self.currentBall = 0
        self.level = 1

    def start(self):

        while True:
            conn, addr = self.socket.accept()
            print("Connected {0}\n{1}".format(str(conn), str(addr)))
            self.numberOfClients += 1
            self.clientsConnected.append(conn)

            #create rcv and send threads
            rcv = ThreadRcv(conn, 'server')
            rcv.queue = queue
            self.rvcThreads.append(rcv)
            #self.rcv.receivedMsg.connect(self.calculatePositions)
            send = ThreadSend(conn, 'server')
            self.sendThreads.append(send)
            self.threads.append(rcv)
            self.threads.append(send)
            #rcv.start()
            #startuj kad se konektuju svi klijenti
            #send.start()
            if self.numberOfClients == 2:
                self.ballsThread.start()

                for t in self.threads:
                    t.start()
                    #t.wait()
                while True:
                    if not queueResponse.empty():
                        responseMsg = str(queueResponse.get())

                        weaponInfo = responseMsg.split('#')[1]
                        if weaponInfo != '':
                            weaponid = weaponInfo.split(',')[0]
                            weaponX = weaponInfo.split(',')[1]
                            if weaponid == '1' and not players[0].bonusNoWeapon:
                                self.Weapon1 = True
                                self.w1X = weaponX
                            elif weaponid == '2'  and not players[1].bonusNoWeapon:
                                self.Weapon2 = True
                                self.w2X = weaponX

                        responseMsg = responseMsg.split('#')[0]
                        orient1 = responseMsg.split(',')[2]
                        orient2 = responseMsg.split(',')[3]
                        if players[0].isAlive:
                            players[0].positionX = int(responseMsg.split(',')[0])

                        if players[1].isAlive:
                            players[1].positionX = int(responseMsg.split(',')[1])
                        # else:
                        #     responseMsg = str(players[0].positionX) + ',' + str(players[1].positionX) + ',' + 'normal,normal'
                        responseMsg = str(players[0].positionX) + ',' + str(players[1].positionX) + ',' + orient1 + ',' +orient2 #+ 'normal,normal'
                        #else:


                        responseMsg += ',' + str(self.w1X) + ',' + str(self.w1Y) + ',' + str(self.w2X) + ',' + str(self.w2Y)

                        responseMsg += ',' + str(players[0].points) + ',' + str(players[1].points) + ',' + str(players[0].lives) + ',' + str(players[1].lives)

                        responseMsg += ',' + str(self.level)

                        #add bonuses to response
                        responseMsg += '@'
                        for bonus in bonuses:
                            responseMsg += bonus.toString() + '@'

                        #add balls to response
                        responseMsg += '#'
                        for ball in balls:
                            responseMsg += ball.toString() + '#'

                        for s in self.sendThreads:
                            s.senderSignal.emit(responseMsg)

    def update(self):
        while True:
            #txt = 'b'
            for ball in balls:
                ball.update()

            if players[0].bonusNoWeapon:
                self.Weapon1 = False
            if players[1].bonusNoWeapon:
                self.Weapon2 = False

            for p in players:
                if p.bonusNoWeapon:
                    p.counterBonus += 1
                    if p.counterBonus == 80:
                        p.counterBonus = 0
                        p.bonusNoWeapon = False

            self.updateWeapons()

            for bonus in bonuses:
                bonus.update()

            self.checkCollisionPlayer()

            self.ballsThread.msleep(32)

    def updateWeapons(self):
        if self.Weapon1:
            self.Weapon1 = self.checkCollisionWeapon(self.w1X, self.w1Y, 0)
            if self.w1Y <= 0:
                self.Weapon1 = False
            else:
                self.w1Y -= WEAPON_SPEED

            if not self.Weapon1:
                self.w1Y = PLAYER_HEIGTH

        if self.Weapon2:
            self.Weapon2 = self.checkCollisionWeapon(self.w2X, self.w2Y, 1)
            if self.w2Y <= 0:
                self.Weapon2 = False
            else:
                self.w2Y -= WEAPON_SPEED

            if not self.Weapon2:
                self.w2Y = PLAYER_HEIGTH


    def checkCollisionWeapon(self, weaponX, weaponY, player_index):
        weaponIsActive = True
        for ball in balls:
            if int(ball.counter) <= int(weaponX) and int(ball.counter) + int(ball.size) >= int(weaponX):
                if int(ball.dy) + int(ball.size) >= int(weaponY):
                    weaponIsActive = False
                    size = ball.size
                    x = ball.counter
                    y = ball.dy
                    balls.remove(ball)
                    #ball.ball.hide()
                    #del ball
                    players[player_index].points += 50
                    self.splitBall(size, x, y)
                    break  # unisti samo jednu lopticu i izadji (pravi bag ako se izostavi -> unistava
        return weaponIsActive


    def checkCollisionPlayer(self):
        for player in players:
            for ball in balls:
                if int(player.positionY) <= int(ball.dy) + int(ball.size)-20:
                    if(int(ball.counter) <= int(player.positionX) and int(player.positionX) <= int(ball.counter) + int(ball.size)) or \
                     (int(ball.counter) <= int(player.positionX) + 25 and int(player.positionX) + 25 <= int(ball.counter) + int(ball.size)) or \
                     (int(ball.counter) <= int(player.positionX) and int(ball.counter) + int(ball.size) >= int(player.positionX) + 28) or \
                     (int(ball.counter) >= int(player.positionX) and int(ball.counter) + int(ball.size) <= int(player.positionX) + 40):

                        if player.lives > 0:
                            player.lives -= 1

                        if player.lives == 0:
                            player.isAlive = False
                            self.w1Y = PLAYER_HEIGTH
                            player.positionX = -100

                        time.sleep(1)
                        self.resetLevel()

            for bonus in bonuses:
                if (int(player.positionX) + int(PLAYER_SIZE) >= int(bonus.x) and float(player.positionY) <= int(bonus.x) \
                        and float(bonus.y) + int(bonus.heigth) >= float(player.positionY)) or \
                        (int(player.positionX) <= int(bonus.x) + int(bonus.width) and int(player.positionX) >= int(bonus.x) and float(bonus.y) + int(bonus.heigth) >= float(player.positionY)):
                    if bonus.type == BONUS_COINS:
                        player.points += COIN_VALUE
                        print('pokupio coin')
                    elif bonus.type == BONUS_NO_WEAPON:
                        print('pokupio ONO DRUGO')
                        if player.Id == 'player1':
                            self.Weapon1 = False
                            player.bonusNoWeapon = True
                        elif player.Id == 'player2':
                            self.Weapon2 = False
                            player.bonusNoWeapon = True

                    bonuses.remove(bonus)

    def splitBall(self, size, x, y):
        if int(size / 2) <= MINBALLSIZE:
            if len(balls) == 0:
                print('prije next leve')
                self.loadNextLevel()
                #self.timer.stop()
                #time.sleep(3)
                #self.loadNextLevel()
        else:
            ball1 = Ball(int(size / 2))
            ball2 = Ball(int(size / 2))

            self.setBallProperties(ball1, x, y, True)
            self.setBallProperties(ball2, x, y, False)

            balls.append(ball1)
            balls.append(ball2)

            if random.randrange(BONUS_RANGE) == 0:
                bonus_type = random.choice(bonus_types)
                bonus = Bonus(x, y, bonus_type)
                bonus.isActive = True
                bonuses.append(bonus)

            ball1.splitedLeft = True
            ball2.splitedRight = True
            ball1.splitedCounter = 42
            ball2.splitedCounter = 42
            ball1.y = ball1.dy
            ball2.y = ball2.dy

    def setBallProperties(self, ball, x, y, isForward):
        ball.counter = x
        ball.dy = y
        ball.forward = isForward

    def resetLevel(self):
        balls.clear()
        bonuses.clear()


        #bonuses.clear()
        if players[0].lives == 0 and players[1].lives == 0:
            return

        for x in range(self.previousBalls):
            temp = x+2
            balls.append(Ball(self.startingBallSize))

            if x % 2 == 0:
                balls[x].x = int(balls[x].x) - 35*temp
                balls[x].counter = int(balls[x].x)
                balls[x].forward = False
            elif x % 2 == 1:
                balls[x].x = int(balls[x].x) + 35*temp
                balls[x].counter = int(balls[x].x)

        self.Weapon1 = False
        self.Weapon2 = False
        self.w1Y = PLAYER_HEIGTH
        self.w2Y = PLAYER_HEIGTH
        queue.put(Qt.Key_Minus)

        #self.currentAmp = AMPLITUDE
        #self.stopOnStart = True
        #self.getReadyLabel.show()
        #self.getReadyLabel.raise_()
        #self.timer.start(20, self)

    def loadNextLevel(self):
        self.level += 1

        nextLevelType = random.choice([0,1])

        bonuses.clear()
        balls.clear()

        if nextLevelType == 0:
            if self.startingBallSize*2 <= MAXBALLSIZE:
                self.startingBallSize = self.startingBallSize*2
                balls.append(Ball(self.startingBallSize))
            else:
                nextLevelType = 1
        if nextLevelType == 1:
            self.previousBalls = self.previousBalls + 1
            temp = self.previousBalls
            for x in range(self.previousBalls):
                balls.append(Ball(self.startingBallSize))
            for b in balls:
                if self.currentBall % 2 == 0:
                    b.x = b.x - 35 * (temp)
                    temp += 1
                    b.counter = math.floor(b.x)
                    b.forward = False
                elif self.currentBall % 2 == 1:
                    b.x = b.x + 35 * (temp)
                    temp += 1
                    b.counter = math.floor(b.x)
                self.currentBall += 1

        #self.stopOnStart = True

        queue.put(Qt.Key_Minus)

        #self.getReadyLabel.show()
        #self.getReadyLabel.raise_()
        #self.levelNumTag.setText(str(self.currentLevel))
        #self.timer.start(20, self)