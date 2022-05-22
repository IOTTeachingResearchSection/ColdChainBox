from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
import pymysql                                                         
import cv2
import time
from RecognizeProcess import RecognizeProcess
import random
import os
import sys


os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
class MyWindow_Window(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow_Window,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("国泰臻鲜")

        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture(0)
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.startCamera()
        self.recognizeProcess = RecognizeProcess()

        self.rootBtn.clicked['bool'].connect(lambda: self.userWidegeHide())
        self.userBtn.clicked['bool'].connect(lambda: self.userWidgeShow())

        self.facilityBtn.clicked.connect(lambda: self.facilityShow())
        self.logBtn.clicked.connect(lambda: self.logShow())
        self.facilityBtn_2.clicked.connect(lambda: self.presonShow())

        self.loginBtn.clicked.connect(self.login)
        self.rootWidget.hide()
        self.manageWidget.hide()
        self.logWidget.hide()
        self.facilityWidget.hide()
        self.personWidget.hide()

        self.handsPass.hide()
        self.facePass.hide()
        self.maskPass.hide()

        self.handsIng.hide()
        self.maskIng.hide()
        self.faceIng.hide()

        self.allPassLabel.hide()

    def presonShow(self):

        self.personWidget.show()
        # self.label_1.setText('用户：刘峰 ID:203080040 注册时间：2022-05-04 08:06:46')
        # self.img_1.setPixmap(QPixmap('/home/young/桌面/001/ColdBox/img/liufeng.png'))

    def logShow(self):

        self.manageWidget.hide()
        self.logWidget.show()
        self.logBtn.clicked.connect(self.manageWidget.hide)
        # self.img_8
        # self.label_11.setText('餐名：木耳菜 ID：20220504016\n放餐人：王思语  ID:193080228 时间：2022-05-04 08:03:29\n取餐人：刘峰 ID:203080040 时间：2022-05-04 23:23:40\n交易哈希：j5oRHGt5TaFEQWDhoUBPA5HAL5dsPanb6kboMeFYUWWk7h')
        # self.img_8.setPixmap(QPixmap('/home/young/桌面/001/ColdBox/img/muercai.png'))
        # self.label_12.setText('餐名：樱桃番茄 ID：20220504016\n放餐人：王艺鑫 ID:203080020 时间：2022-05-05 09:31:12\n取餐人：刘峰 ID:203080040 时间：2022-05-05 21:00:16\n交易哈希：j5jHkXXanhm76MWVtX5rzwqYM2BZ53CevZcan9P1wJyPKW')
        # self.img_9.setPixmap(QPixmap('/home/young/桌面/001/ColdBox/img/ytfq.png'))
    
    def facilityShow(self):

        water = str(random.randint(85,90))
        tmp = str((random.randint(195,205))/100)
        self.manageWidget.hide()
        self.facilityWidget.show()
        self.waterNumber.display(water)
        self.tmpNumber.display(tmp)


    def passLabelShow(self,faceState,maskState,glovesState):

        if faceState: #人脸通过

            self.facePass.show()
            self.handsIng.hide()
            self.maskIng.show()
            self.faceIng.hide()

            if maskState: #人脸 + 口罩通过

                self.handsIng.hide()
                self.maskIng.hide()
                self.faceIng.hide()
                self.maskPass.show()
                self.handsIng.show()

                if glovesState: # 人脸 + 口罩 + 手套通过

                    self.handsIng.hide()
                    self.handsPass.show()
                    self.allPassLabel.show()
                    
            else: #人脸通过 + 口罩不通过

                self.maskPass.hide()
                self.maskIng.show()


        else: #人脸不通过
 
            self.faceIng.show()
            self.handsPass.hide()
            self.facePass.hide()
            self.maskPass.hide()
            self.maskIng.hide()
            self.handsIng.hide()
            self.allPassLabel.hide()
        


    def startCamera(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            
            # flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            self.timer_camera.start(1)  # 定时器开始计时30ms，结果是每过1ms从摄像头中取一帧显示
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流

        self.timer_camera.timeout.connect(self.camera)  # 若定时器结束，则调用camera()


    def camera(self):

        self.image = self.cap.read()[1]  # 从视频流中读取

        self.recognizeProcess.process(self.image)
        self.passLabelShow(self.recognizeProcess.facePass,self.recognizeProcess.maskPass,self.recognizeProcess.glovesPass)
        
        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.video.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage


    def login(self):
            conn = pymysql.connect(host='localhost', database='coldboxtest', user='root', password='123456', charset='utf8')
            cursor = conn.cursor()
            username = self.le_user.text()
            password = self.le_passwd.text()
            sql = 'SELECT username, password FROM rootuser WHERE username=%s'
            cursor.execute(sql, (username,))
            data = cursor.fetchone()
            if username and password:
                    if data:
                            if data[1] == password:
                                    QMessageBox.information(self, "登录", "密码正确, 确认登录.", QMessageBox.Yes)
                                    self.rootWidget.hide()
                                    self.rootBtn.hide()
                                    self.userBtn.hide()
                                    self.manageWidget.show()
                                    self.le_user.setText('')
                                    self.le_passwd.setText('')
                            else:
                                    QMessageBox.warning(self, "警告！", "用户名或者密码错误！", QMessageBox.Yes)
                                    self.le_passwd.setText('')
                    else:
                            QMessageBox.warning(self, "警告！", "用户名或者密码错误！", QMessageBox.Yes)
                            self.le_user.setText('')
                            self.le_passwd.setText('')
            elif username:
                    QMessageBox.warning(self, "警告！", "密码不能为空！", QMessageBox.Yes)
            else:
                    QMessageBox.warning(self, "警告！", "用户名不能为空！", QMessageBox.Yes)


    def userWidegeHide(self):
        self.userWidget.hide()
        self.timer_camera.stop()  # 关闭定时器
        self.cap.release()
        # self.video.clear()

    def userWidgeShow(self):
        self.userWidget.show()
        self.cap = cv2.VideoCapture(0)
        self.startCamera()


if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    ui=MyWindow_Window()
    ui.show()
    sys.exit(app.exec_())
