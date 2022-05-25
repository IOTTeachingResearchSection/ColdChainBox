from PyQt5.QtCore import QThread, pyqtSignal, QMutex
# from playsound import playsound
import pygame
from Lock.Lock import Lock
import time
from JDChain.Chain import Chain
from MySql.MySql import MySql
from Uploadimg.Uploadimg import Uploadimg
from Rfid.Rfid import Rfid

voiceThreadLock = QMutex() #线程锁

def playsound(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

class FacePassVoicePlay(QThread):


    def __init__(self) -> None:
        super().__init__()


    def run(self):
        voiceThreadLock.lock()
        
        print('face Threading.........')
        playsound('voice/FacePass.mp3')
        time.sleep(1)

        voiceThreadLock.unlock()

        
class MaskVoicePlay0(QThread):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        voiceThreadLock.lock()

        print('mask0 Threading.........')
        playsound('voice/Maskstate0.mp3')
        time.sleep(1)

        voiceThreadLock.unlock()
        
class MaskVoicePlay1(QThread):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        voiceThreadLock.lock()

        print('mask1 Threading.........')
        playsound('voice/Maskstate-1.mp3')
        time.sleep(1)

        voiceThreadLock.unlock()

class MaskPassVoicePlay(QThread):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        voiceThreadLock.lock()

        print('maskpass Threading.........')
        playsound('voice/MaskPass.mp3')
        time.sleep(1)

        voiceThreadLock.unlock()

class GlovesPassVoicePlay(QThread):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        voiceThreadLock.lock()

        print('glovespass Threading.........')
        playsound('voice/GlovesPass.mp3')
        time.sleep(2)
        playsound('voice/LockOpen.mp3')
        voiceThreadLock.unlock()

class GlovesVoicePlay(QThread):

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        voiceThreadLock.lock()

        print('gloves Threading.........')
        playsound('voice/Glovesstate0.mp3')
        time.sleep(1)

        voiceThreadLock.unlock()


class OpenLock(QThread):
    
    def __init__(self) -> None:
        super().__init__()
        self.lock = Lock()
        self.uploadimg = Uploadimg()
        self.lockThreadLock = QMutex() 
        self.targetID = None        
        self.glovesUrl = None

    def run(self):

        self.lockThreadLock.lock()
        
        time.sleep(2)
        print('lock Threading.........')
        self.lock.open()   #开锁
        # playsound('voice/LockOpen.mp3')
        print('门开了，开门人是：')
        print(self.targetID)
       
        self.lockThreadLock.unlock()


class GetRFID(QThread):

    def __init__(self) -> None:
        super().__init__()
        # self.rfid = RFID()
        self.rfidThreadLock = QMutex()
        self.mysql = MySql()
        self.chain = Chain()
        self.userID = None   #放餐人ID
        self.faceUrl = None
        self.maskUrl = None
        self.glovesUrl = None
        self.rfid = Rfid()
        self.cardSet = self.rfid.allCard()

    def difCard(self,set1, set2): #remova card and add card
        remove = list(set1 - set2)
        add = list(set2 - set1)
        return add,remove

    def run(self):
        self.rfidThreadLock.lock()
        self.uploadimg = Uploadimg()
        cardSet = self.rfid.allCard()
        print('cardSet',cardSet)
        print('self',self.cardSet)
        if cardSet != self.cardSet:
            addedCards,removedCards = self.difCard(self.cardSet,cardSet)
            print('addedCards',addedCards)
            print('removedCards',removedCards)
            self.cardSet = cardSet

            if addedCards != []:
                for i in addedCards:
                        #数据库中写入放餐人姓名 + 时间
                    now = time.time()
                    user = self.mysql.query(self.userID,'user')
                    self.mysql.updata(i,puttime=now,putpeople=user['name'],putpeopleid=self.userID)
                    data = self.mysql.query(i)
                    try:
                        self.chain.insert(data)
                    except Exception as e:
                        print(e)

            if removedCards != []:
                for i in removedCards:
                    now = time.time()
                    user = self.mysql.query(self.userID,'user')
                    self.mysql.updata(i,gettime=now,getpeople=user['name'],getpeopleid=self.userID)
                    try:
                        self.faceUrl = self.uploadimg.upload_img('./recognize_img/'+ self.userID + '/face.png')
                        self.maskUrl = self.uploadimg.upload_img('./recognize_img/'+ self.userID + '/mask.png')
                        self.glovesUrl = self.uploadimg.upload_img('./recognize_img/'+ self.userID + '/gloves.png')
                    except Exception as e:
                        print(e)

                    print('faceUrl',self.faceUrl)

                    self.mysql.updata(i,faceurl=self.faceUrl,maskurl=self.maskUrl,glovesurl=self.glovesUrl)
                    _,olddata = self.chain.query(i)
                    print('--------------------')
                    print(type(olddata))
                    print(olddata)
                    print('--------------------')
                    newdata = {
                        'gettime':now,
                        'getpeople':user['name'],
                        'getpeopleid':self.userID,
                        'faceurl':self.faceUrl,
                        'maskurl':self.maskUrl,
                        'glovesurl':self.glovesUrl
                    }
                    data = dict(olddata, **newdata)
                    self.chain.udpata(data)
        else:
            print('None')
        self.rfidThreadLock.unlock()

