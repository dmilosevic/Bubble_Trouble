#from Server import queue, queueResponse, Server, w1X, w2X, Weapon1, Weapon2 #*
from multiprocessing import Process
import Server as s
from ThreadRcv import *
from Common.Settings import *
from PyQt5.QtCore import Qt, QBasicTimer
import time


def calculatePositions(q: Queue, qResp: Queue):
    responseMsg = ''
    PositionXP1 = 50
    PositionXP2 = 700



    Weapon1Y = WINDOWHEIGHT-80
    Weapon2Y = WINDOWHEIGHT-80

    Player1Orientation = 'normal'
    Player2Orientation = 'normal'
    timer = QBasicTimer()
    while True:
        weaponInfo = '#'

        if not q.empty():
            rez = str(q.get())
            if rez == '1':
                responseMsg = str(WINDOWWIDTH/2) + ',' + Player1Orientation
                PositionXP1 = int(responseMsg)
            elif rez == '2':
                #responseMsg = '50,700,' + Player1Orientation + ',' + Player2Orientation
                PositionXP1 = 50
                PositionXP2 = 700
            elif rez == '3':
                #responseMsg = '50,700,' + Player1Orientation + ',' + Player2Orientation
                PositionXP1 = 50
                PositionXP2 = 700

            else:
                if int(rez) == Qt.Key_Right:
                    Player1Orientation = 'right'
                    if PositionXP1 + PLAYER_SIZE < WINDOWWIDTH - 13:
                        PositionXP1 += 5
                        #responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation
                if int(rez) == Qt.Key_Left:
                    Player1Orientation = 'left'
                    if PositionXP1 - 5 > 20:
                        PositionXP1 -= 5
                        #responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation
                if int(rez) == Qt.Key_Space:
                    weaponInfo += '1,' + str(PositionXP1)
                        #responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation

                if int(rez) == Qt.Key_A:
                    Player2Orientation = 'left'
                    if PositionXP2 - 5 > 20:
                        PositionXP2 -= 5
                        #responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation
                if int(rez) == Qt.Key_D:
                    Player2Orientation = 'right'
                    if PositionXP2 + PLAYER_SIZE < WINDOWWIDTH - 13:
                        PositionXP2 += 5
                        #responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation
                if int(rez) == Qt.Key_Shift:
                    weaponInfo += '2,' + str(PositionXP2)
                if int(rez) == Qt.Key_Minus:
                    PositionXP1 = 50
                    PositionXP2 = 700
                    Player1Orientation = 'normal'
                    Player2Orientation = 'normal'

                    #responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation

            #s.Weapon1, Weapon1Y, s.Weapon2, Weapon2Y = updateWeapons(s.Weapon1, s.Weapon2, Weapon1Y, Weapon2Y)
            responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation + weaponInfo
            #responseMsg += ',' + str(s.w1X) + ',' + str(s.w1Y) + ',' + str(s.w2X) + ',' + str(s.w2Y)

            qResp.put(responseMsg)
        else:
            #s.Weapon1, Weapon1Y, s.Weapon2, Weapon2Y = updateWeapons(s.Weapon1, s.Weapon2, Weapon1Y, Weapon2Y)

            responseMsg = str(PositionXP1) + ',' + str(PositionXP2) + ',' + Player1Orientation + ',' + Player2Orientation +weaponInfo
            #responseMsg += ',' + str(s.w1X) + ',' + str(s.w1Y) + ',' + str(s.w2X) + ',' + str(s.w2Y)

            qResp.put(responseMsg)
            time.sleep(0.032)


             #elif key == Qt.Key_Minus:
                #self.drawPlayer('normal')
                #self.player.setGeometry(self.PositionX, self.PositionY, self.Width, self.Heigth)


if __name__ == '__main__':

    process = Process(target=calculatePositions, args=[s.queue, s.queueResponse])
    process.start()
    print('pokrenuo proces')
    serv = s.Server()
    serv.start()
    print('pokrenuo server')
