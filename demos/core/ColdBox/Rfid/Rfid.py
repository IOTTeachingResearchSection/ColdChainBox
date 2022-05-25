from Rfid.RfidReader import RfidReader
from threading import Timer
import  threading



class Rfid:

    def __init__(self):
        self.read = RfidReader()
        self.prevCards = set()

    def delayCheck(self):
        currCards = self.read.getCardSet()
        self.prevCards = currCards

    def allCard(self):
        self.read.queryCards()
        timer = Timer(3, self.delayCheck)
        timer.start()
        timer.join()
        return self.prevCards

    def readSleep(self):
        self.read.killReadHandler()

    def readWakeup(self):
        self.read.aliveReadHandler()

if __name__ == '__main__':
    rfid = Rfid()
    print(rfid.allCard())



# print(threading.enumerate())
#
# r = RfidReader()
#
# print(threading.enumerate())
# prevCards = set()
#
#
# def delayCheck():
#     print('delay')
#     global prevCards
#     currCards = r.getCardSet()
#     addedCards = currCards - prevCards
#     removedCards = prevCards - currCards
#     print(f'addedCards: {addedCards}')
#     print(f'removedCards: {removedCards}')
#     print(f'currCards: {currCards}')
#     print('新增或移走卡后，点击键盘继续')
#     prevCards = currCards
#
# if __name__ == '__main__':
#
#
#     while True:
#         i = int(input('input:'))
#         r.put_alive()
#         if i == 1:
#             r.queryCards()
#             timer = Timer(3, delayCheck)
#             timer.start()
#             timer.join()
#         elif i == 0:
#             r.put_alive()
#             r.killReadHandler()
#
#
#
#         elif i == 2:
#             r.put_alive()
#             r.aliveReadHandler()
#
#         else:
#             break
#
#     print('main end')
#     print(threading.enumerate())



# if __name__ == '__main__':
#     r = RfidReader()
#     lena = cv2.imread('1.png')
#     cv2.imshow('image', lena)
#     prevCards = set()
#
#     def delayCheck():
#         global prevCards
#         currCards = r.getCardSet()
#         addedCards = currCards - prevCards
#         removedCards = prevCards - currCards
#         print(f'addedCards: {addedCards}')
#         print(f'removedCards: {removedCards}')
#         print(f'currCards: {currCards}')
#         print('新增或移走卡后，点击键盘继续')
#         prevCards = currCards
#
#     r.queryCards()
#     timer = Timer(2, delayCheck)
#     timer.start()
#
#     cv2.waitKey(0)
#
#     r.queryCards()
#     timer = Timer(2, delayCheck)
#     timer.start()
#
#     cv2.waitKey(0)
#
#     r.queryCards()
#     timer = Timer(2, delayCheck)
#     timer.start()
#
#     cv2.waitKey(0)
#
#     r.queryCards()
#     timer = Timer(2, delayCheck)
#     timer.start()
#
#     cv2.waitKey(0)
#     r.killReadHandler()

