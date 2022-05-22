# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import cv2
from Mask import Mask


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture(0)
        self.startCamera()
        self.gloves = Mask()




    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.userWidget = QtWidgets.QWidget(self.centralwidget)
        self.userWidget.setGeometry(QtCore.QRect(0, 60, 800, 500))
        self.userWidget.setObjectName("userWidget")
        self.textLine = QtWidgets.QTextEdit(self.userWidget)
        self.textLine.setEnabled(False)
        self.textLine.setGeometry(QtCore.QRect(640, 10, 155, 480))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.textLine.setFont(font)
        self.textLine.setObjectName("textLine")

        #视频
        self.video = QtWidgets.QLabel(self.userWidget)
        self.video.setGeometry(QtCore.QRect(0, 10, 640, 480))
        self.video.setFrameShape(QtWidgets.QFrame.Box)
        self.video.setText("")
        self.video.setTextFormat(QtCore.Qt.PlainText)
        self.video.setObjectName("video")

        self.rootWidge = QtWidgets.QWidget(self.centralwidget)
        self.rootWidge.setGeometry(QtCore.QRect(0, 60, 800, 500))
        self.rootWidge.setObjectName("rootWidge")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 241, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.userBtn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userBtn.sizePolicy().hasHeightForWidth())
        self.userBtn.setSizePolicy(sizePolicy)
        self.userBtn.setObjectName("userBtn")
        self.horizontalLayout.addWidget(self.userBtn)
        self.rootBtn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootBtn.sizePolicy().hasHeightForWidth())
        self.rootBtn.setSizePolicy(sizePolicy)
        self.rootBtn.setObjectName("rootBtn")
        self.horizontalLayout.addWidget(self.rootBtn)
        self.rootWidge.raise_()
        self.userBtn.raise_()
        self.rootBtn.raise_()
        self.userWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.userBtn.clicked['bool'].connect(lambda: self.userWidgeShow())
        self.userBtn.clicked['bool'].connect(self.rootWidge.hide)
        self.rootBtn.clicked['bool'].connect(self.rootWidge.show)
        self.rootBtn.clicked['bool'].connect(lambda: self.userWidegeHide())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def userWidegeHide(self):
        self.userWidget.hide()
        self.timer_camera.stop()  # 关闭定时器
        self.cap.release()
        # self.video.clear()

    def userWidgeShow(self):
        self.userWidget.show()
        self.cap = cv2.VideoCapture(0)
        self.startCamera()

    def startCamera(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            
            self.timer_camera.start(1)  # 定时器开始计时30ms，结果是每过1ms从摄像头中取一帧显示
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流

        self.timer_camera.timeout.connect(self.camera)  # 若定时器结束，则调用camera()


    def camera(self):


        self.image = self.cap.read()[1]  # 从视频流中读取

        self.gloves.run(self.image)

        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.video.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textLine.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:400;\"><br /></p></body></html>"))
        self.userBtn.setText(_translate("MainWindow", "用户"))
        self.rootBtn.setText(_translate("MainWindow", "管理员"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(w)
    w.show()
    sys.exit(app.exec())
