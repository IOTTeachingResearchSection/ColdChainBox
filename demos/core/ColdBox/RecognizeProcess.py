from Mask.Mask import Mask
from Face.Face import Face
from Gloves.Gloves import Gloves
from Thread import FacePassVoicePlay, GlovesPassVoicePlay, GlovesVoicePlay, MaskPassVoicePlay, MaskVoicePlay1, MaskVoicePlay0, OpenLock, GetRFID
import time
import cv2
import os
from MySql.MySql import MySql
from openvino.inference_engine import IECore


#   QTherad
class RecognizeProcess:

    def __init__(self) -> None:


        self.facePass = False
        self.maskPass = False
        self.glovesPass = False
        self.glovesFirst = True

        self.facePassVoicePlay = FacePassVoicePlay()
        self.maskPassVoicePlay = MaskPassVoicePlay()
        self.glovesPassVoicePlay = GlovesPassVoicePlay()

        self.openLock = OpenLock()
        self.getrfid = GetRFID()

        self.maskVoicePlay0 = MaskVoicePlay0()
        self.maskVoicePlay1 = MaskVoicePlay1()
        self.glovesVoicePlay = GlovesVoicePlay()
        
        ie = IECore()
        self.mask = Mask(ie)
        self.face = Face()
        self.gloves = Gloves(ie)

        self.facePassTime = time.time()
        self.maskPassTime = time.time()

        self.targetID = None
        self.mysql = MySql()
        self.putUser = self.mysql.queryAll()
        
        self.faceThread = True
        self.maskstate = None
        self.glovesstate = None
        self.maskFirstPass = 0
        self.getTime = None
        self.allRecognizeFinish = False


    def goProcess(self,image):
        if self.facePass and time.time() - self.facePassTime > 2: #识别通过后延时两秒后进入口罩
            if time.time() - self.facePassTime > 60:   #人脸识别后有效时间
                self.facePass = False
                self.maskPass = False
                self.glovesPass = False
                self.glovesFirst = True

                self.maskstate = None
                self.glovesstate = None

                self.faceThread = True

                self.maskFirstPass = 0

            else:
                if self.maskPass and time.time() - self.maskPassTime > 2:
                    self.gloves.run(image)
                     #print(self.glovesstate ,self.gloves.glovesState)
                    if self.glovesstate != self.gloves.glovesState :
                        self.glovesstate = self.gloves.glovesState
                        if not self.gloves.glovesState:
                            
                            self.glovesVoicePlay.start()
                            
                            
                    elif self.gloves.glovesState and self.glovesFirst:
                        self.glovesPassVoicePlay.start()
                        self.openLock.targetID = self.targetID
                        self.openLock.start()
                        self.getrfid.userID = self.targetID
                        
                        self.glovesPass = True
                        self.glovesFirst = False
                        self.openLock.start()
                        self.allRecognizeFinish = True 
                        self.getTime = time.time()
                        cv2.imwrite('./recognize_img/'+ self.targetID + '/gloves.png', image) 
                        
                else:
                    self.mask.run(image)
                    if self.maskstate != self.mask.recognizeState:

                        self.maskstate = self.mask.recognizeState
                        if self.mask.recognizeState == 0:
                            self.maskVoicePlay0.start()
                            self.maskPass = False
                            self.maskFirstPass = 0
                        elif self.mask.recognizeState == -1:
                            self.maskVoicePlay1.start()
                            self.maskPass = False
                            self.maskFirstPass = 0
                    elif self.mask.recognizeState == 1:
                        self.maskFirstPass += 1
                        if self.maskFirstPass == 1:
                            cv2.imwrite('./recognize_img/'+ self.targetID + '/mask.png', image)
                            self.maskPass = True
                            self.maskPassTime = time.time()
                        if time.time() - self.maskPassTime > 1.5:
                            self.maskPassVoicePlay.start()



        else:
            self.face.discernFace(image)
            if self.face.recognizedID in self.putUser and self.faceThread:
                self.targetID = self.face.recognizedID 

                if not os.path.exists('./recognize_img/'+ self.targetID):
                    os.mkdir('./recognize_img/'+ self.targetID)

                cv2.imwrite('./recognize_img/'+ self.targetID +'/face.png', image)
                self.faceThread = False
                self.facePassVoicePlay.start()
                self.facePassTime = time.time()
                self.face.recognizedID = None
                self.facePass = True
            if not self.faceThread:
                self.face.recognizedID = None

    def getProcess(self):
        if time.time() - self.getTime > 60:
            self.allRecognizeFinish = False
        # if (time.time() - self.getTime) % 2 == 0:   #开门后读取RFID
        elif (time.time() - self.getTime) > 3:
            self.getrfid.start()

    def process(self,image):
        if self.allRecognizeFinish:
            self.getProcess()
        else:
            self.goProcess(image)



"""
#python 原生线程

class RecognizeProcess:

    def __init__(self) -> None:
        self.facePass = False
        self.mask = MaskVideo()
        self.face = Face()
        self.now = time.time()
        self.__maskThreadLock = threading.RLock() #设置线程锁
        self.__faceThreadLock = threading.RLock() #设置线程锁
        self.faceThread = True
        self.maskThread = True
        self.maskstate = None

    def facePassVoicePlay(self):
        self.__faceThreadLock.acquire()
        playsound('voice/FacePass.mp3')
        self.__faceThreadLock.release()

    def maskVoicePlay0(self):
        self.__maskThreadLock.acquire() #请求锁
        playsound('voice/Maskstate0.mp3')
        self.maskThread = True
        time.sleep(1.5)
        self.__maskThreadLock.release() #释放锁


    def maskVoicePlay1(self):
        self.__maskThreadLock.acquire() #请求锁
        playsound('voice/Maskstate-1.mp3')
        self.maskThread = True
        time.sleep(1.5)
        self.__maskThreadLock.release() #释放锁
        

    def goProcess(self,image):
        if self.facePass and time.time() - self.now > 2:
            if time.time() - self.now > 20:
                self.facePass = False
                self.maskstate = None
                self.faceThread = True

            else:
                self.mask.run(image)

                # print('self.maskState:',self.maskstate)
                # print('self.mask.recognizeState:',self.mask.recognizeState)
                if self.maskstate != self.mask.recognizeState:

                    self.maskstate = self.mask.recognizeState
                    if self.mask.recognizeState == 0 and self.maskThread:
                        self.maskThread = False
                        maskVoicePlay = threading.Thread(target=self.maskVoicePlay0)
                        maskVoicePlay.setDaemon(True)  #设置守护线程，主线程关闭，子线随及关闭
                        maskVoicePlay.start()
                    elif self.mask.recognizeState == -1 and self.maskThread:
                        self.maskThread = False
                        maskVoicePlay = threading.Thread(target=self.maskVoicePlay1)
                        maskVoicePlay.setDaemon(True)  #设置守护线程，主线程关闭，子线随及关闭
                        maskVoicePlay.start()


        else:
            self.face.discernFace(image)
            if self.face.recognizedID == '513021200006080330' and self.faceThread:
                print('faceing.........')
                self.faceThread = False
                faceVoicePlay = threading.Thread(target=self.facePassVoicePlay)
                faceVoicePlay.setDaemon(True)  #设置守护线程，主线程关闭，子线随及关闭
                faceVoicePlay.start()
                self.now = time.time()
                self.face.recognizedID = None
                self.facePass = True
            if not self.faceThread:
                self.face.recognizedID = None

"""


# from VoiceTest import Voice,StoppableThread
# from playsound import playsound
# from PyQt5.QtCore import QThread, pyqtSignal
# import threading

# class RecognizeProcess(QThread):
#     def __init__(self,image) -> None:
#         super().__init__()
#         self.image = image
#         self.mask = MaskVideo()
#         self.face = Face()
#         self.voice = Voice()
#         self.stopThread = StoppableThread()
#         self.facePass = False
#         self.__now = None
#         self.id = '513021200006080330'
    
#     def run(self):
#         if self.facePass:
#             print('线程，口罩识别')
#             self.mask.run(self.image)
#             print('口罩识别状态：',self.mask.recognizeState)
#             if self.mask.recognizeState == 0:
#                 playsound('voice/Maskstate0.mp3')
#             elif self.mask.recognizeState  == -1:
#                 playsound('voice/Maskstate-1.mp3')

#             print(time.time() - self.__now)
#             if time.time() - self.__now > 5:
#                 self.facePass = False
#                 self.__now = None
            
#         else:
#             print('线程，人脸识别')
#             self.face.discernFace(self.image)
#             print(self.face.recognizedID)
#             if self.id == self.face.recognizedID:
#                 playsound('voice/FacePass.mp3')
#                 self.facePass = True
#             if self.facePass:
#                 self.__now = time.time()

#         self.sleep(1)
                

#         self.__recognizeThread.release()

#         self.__threadState = False

#     def goProcessThread(self,image):

#         if not self.__threadState:
#             thread = threading.Thread(target=self.goProcess,args=(image,))
#             thread.setDaemon(True)
#             thread.start()



# class RecognizeProcess:

#     def __init__(self) -> None:

#         self.mask = MaskVideo()
#         self.face = Face()
#         self.voice = Voice()
#         self.stopThread = StoppableThread()
#         self.facePass = False
#         self.__now = None
#         self.__recognizeThread = threading.RLock() 
#         self.__threadState = False
#         self.id = '513021200006080330'

#     def goProcess(self,image):

#         self.__threadState = True

#         self.__recognizeThread.acquire() #请求锁
#         if self.facePass:
#             print('线程，口罩识别')
#             self.mask.run(image)

#             print('口罩识别状态：',self.mask.recognizeState)
#             if self.mask.recognizeState == 0:
#                 playsound('voice/Maskstate0.mp3')
#             elif self.mask.recognizeState  == -1:
#                 playsound('voice/Maskstate-1.mp3')

#             print(time.time() - self.__now)
#             if time.time() - self.__now > 10:
#                 self.facePass = False
#                 self.__now = None
            
#         else:
#             print('线程，人脸识别')
#             self.face.discernFace(image)
#             print(self.face.recognizedID)
#             if self.id == self.face.recognizedID:
#                 playsound('voice/FacePass.mp3')
#                 self.facePass = True
#             if self.facePass:
#                 self.__now = time.time()
                

#         self.__recognizeThread.release()

#         self.__threadState = False

#     def goProcessThread(self,image):

#         if not self.__threadState:
#             thread = threading.Thread(target=self.goProcess,args=(image,))
#             thread.setDaemon(True)
#             thread.start()


# class RecognizeProcess:

#     def __init__(self) -> None:

#         self.mask = MaskVideo()
#         self.face = Face()
#         self.voice = Voice()
#         self.stopThread = StoppableThread()
#         self.facePass = False
#         self.__now = None
#         self.__recognizeThread = threading.RLock() 
#         self.__threadState = False
#         self.id = '513021200006080330'

#     def goProcess(self,image):

#         if self.facePass:
#             self.mask.run(image)
#             # print(self.mask.recognizeState)
#             #maskVoicePlay: 口罩播报线程
#             print(self.voice.maskThreadState)
#             if not self.voice.maskThreadState:
#                 print(self.mask.recognizeState)
#                 maskVoicePlay = threading.Thread(target=self.voice.maskState,args=(self.mask.recognizeState,))
#                 maskVoicePlay.setDaemon(True)  #设置守护线程，主线程关闭，子线随及关闭
#                 maskVoicePlay.start()
#             print(time.time() - self.__now)
#             if time.time() - self.__now > 5:
#                 self.facePass = False
#                 self.__now = None
#                 # self.stopThread.stop() 
            
#         else:
#             self.face.discernFace(image)
#             print(self.voice.faceThreadState)
#             if not self.voice.faceThreadState:
#                 faceVoicePlay = threading.Thread(target=self.voice.faceJudge,args=(self.face.recognizedID,))
#                 faceVoicePlay.setDaemon(True)  #设置守护线程，主线程关闭，子线随及关闭
#                 faceVoicePlay.start()
#             print(self.facePass )
#             self.facePass = self.voice.facePass
#             if self.facePass:
#                 self.voice.facePass = False
#                 self.face = Face()
#                 self.__now = time.time()
