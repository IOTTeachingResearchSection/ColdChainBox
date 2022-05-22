"""
人脸考勤系统（可以运行在CPU）
1、人脸检测：
2、注册人脸，将人脸特征存储进feature.csv
3、识别人脸，将考勤数据存进attendance.csv
"""

# 导入包
import cv2
import numpy as np
import dlib
import time
import csv
from argparse import ArgumentParser

class Face:

    def __init__(self) -> None:
        # 加载人脸检测器
        self.hog_face_detector = dlib.get_frontal_face_detector()
        self.cnn_detector = dlib.cnn_face_detection_model_v1('/home/pi/Desktop/ColdBox/Face/face_weights/mmod_human_face_detector.dat')
        self.haar_face_detector  = cv2.CascadeClassifier('/home/pi/Desktop/ColdBox/Face/face_weights/haarcascade_frontalface_default.xml')

        # 加载关键点检测器
        self.points_detector = dlib.shape_predictor('/home/pi/Desktop/ColdBox/Face/face_weights/shape_predictor_68_face_landmarks.dat')
        # 加载resnet模型
        self.face_descriptor_extractor = dlib.face_recognition_model_v1('/home/pi/Desktop/ColdBox/Face/face_model/dlib_face_recognition_resnet_model_v1 .dat')
        self.recognizedID = None #已识别出的人

    def faceRegiser(self,faceId=1,userName='default',interval=3,faceCount=3,resize_w=0,resize_h=0):
        # 计数
        count = 0
        # 开始注册时间
        startTime = time.time()
        # 视频时间
        frameTime = startTime
        # 控制显示打卡成功的时长
        # 打开文件
        f =  open('/home/pi/Desktop/ColdBox/Face/face_data/feature.csv','a',newline='')
        csv_writer = csv.writer(f)
        cap = cv2.VideoCapture(0)
        if resize_w == 0 or resize_h == 0:
            resize_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))//2
            resize_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) //2
        while True:
            ret,frame = cap.read()
            # frame = cv2.resize(frame,(resize_w,resize_h))  #裁剪视频尺寸
            # frame = cv2.flip(frame,1)  #视频图像水平翻转
            # 检测
            face_detetion = self.hog_face_detector(frame,1) #人脸检测
            for face in face_detetion:
                # 识别68个关键点
                points = self.points_detector(frame,face)  #加载关键点检测器 返回68个关键点  face开始内部形状预测的边界框
                # 绘制人脸关键点
                for point in points.parts():
                    cv2.circle(frame,(point.x,point.y),2,(255,0,255),1)
                # 绘制框框
                l,t,r,b = face.left(),face.top(),face.right(),face.bottom()
                cv2.rectangle(frame,(l,t),(r,b),(0,255,0),2)
                now = time.time()
                # if  (now - show_time) < 0.5:
                #     frame = cv2AddChineseText(frame, "注册成功 {count}/{faceCount}".format(count=(count+1),faceCount=faceCount) ,  (l, b+30), textColor=(255, 0, 255), textSize=40)
                # # 检查次数
                if count < faceCount:
                    # 检查时间
                    if now - startTime > interval:
                        # 特征描述符
                        face_descriptor = self.face_descriptor_extractor.compute_face_descriptor(frame,points)
                        face_descriptor = [f for f in face_descriptor ]
                        # 描述符增加进data文件
                        line = [faceId,userName,face_descriptor]
                        # 写入
                        csv_writer.writerow(line)  #保存
                        # 保存照片样本
                        print('人脸注册成功 {count}/{faceCount}，工作证件编号:{faceId}，注册人姓名:{userName}'.format(count=(count+1),faceCount=faceCount,faceId=faceId,userName=userName))
                        # frame = cv2AddChineseText(frame, "注册成功 {count}/{faceCount}".format(count=(count+1),faceCount=faceCount) ,  (l, b+30), textColor=(255, 0, 255), textSize=40)
                        show_time = time.time()
                        # 时间重置
                        startTime = now
                        # 次数加一
                        count +=1
                else:
                    print('人脸注册完毕')
                    return
                # 只取其中一张脸
                break
            now = time.time()
            fpsText = 1 / (now - frameTime)
            frameTime = now

            cv2.imshow('FaceRegiser',frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        f.close()
        cap.release()
        cv2.destroyAllWindows()


# 返回DLIB格式的face
    def getDlibRect(self,detector='hog',face=None):
        l,t,r,b = None,None,None,None
        if detector == 'hog':
            l,t,r,b = face.left(),face.top(),face.right(),face.bottom()
        if detector == 'cnn':
            l = face.rect.left()
            t = face.rect.top()
            r = face.rect.right()
            b = face.rect.bottom()
        if detector == 'haar':
            l = face[0]
            t = face[1]
            r = face[0] + face[2]
            b = face[1] + face[3]
        nonnegative = lambda x : x if x >= 0 else 0  
        return map(nonnegative,(l,t,r,b ))

# 获取CSV中信息
    def getFeatList(self):
        # print('开启识别中...')
        feature_list = None
        label_list = []
        name_list = []
        # 加载保存的特征样本
        with open('/home/pi/Desktop/ColdBox/Face/face_data/feature.csv','r',encoding = 'utf-8') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                # 重新加载数据
                faceId = line[0]
                userName = line[1]
                face_descriptor = eval(line[2])
                label_list.append(faceId)
                name_list.append(userName)
                # 转为numpy格式
                face_descriptor = np.asarray(face_descriptor,dtype=np.float64)
                # 转为二维矩阵，拼接
                face_descriptor = np.reshape(face_descriptor,(1,-1))
                # 初始化
                if feature_list is None:
                    feature_list = face_descriptor
                else:
                    # 拼接
                    feature_list = np.concatenate((feature_list,face_descriptor),axis=0)
        # print("开启识别")
        return feature_list,label_list,name_list

    # 人脸识别
    def faceRecognize(self,image,detector='haar',threshold=0.5):

        """
        image: frame ,cap.read()[1]
        """

        
        # 视频时间
        global face_detetion

        # 加载特征
        feature_list,label_list,name_list = self.getFeatList()
        face_time_dict = {}
        # 保存name,time人脸信息
        face_info_list = []
        # numpy格式人脸图像数据
        face_img_list = []
        # 统计人脸数
        face_count = 0

        # 考勤记录
        f = open('/home/pi/Desktop/ColdBox/Face/face_data/attendance.csv','a',encoding = 'utf-8')
        csv_writer = csv.writer(f)
        
        # cap = cv2.VideoCapture(0)

        frame = image
        # print(type(frame))

        # 切换人脸检测器
        if detector == 'hog':
            face_detetion = self.hog_face_detector(frame,1)
        if detector == 'cnn':
            face_detetion = self.cnn_detector(frame,1)
        if detector == 'haar':   
            frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
            face_detetion = self.haar_face_detector.detectMultiScale(frame_gray,minNeighbors=7,minSize=(100,100))  #检测出图片中所有的人脸，并将人脸用vector保存各个人脸的坐标、大小（用矩形表示）
        # person_detect = len(face_detetion)

        for face in face_detetion:
            l,t,r,b = self.getDlibRect(detector,face)
            face = dlib.rectangle(int(l),int(t),int(r),int(b))
            # 识别68个关键点
            points = self.points_detector(frame,face)
            cv2.rectangle(frame,(l,t),(r,b),(0,255,0),2)
            # 人脸区域
            face_crop = frame[t:b,l:r]
            #特征
            face_descriptor = self.face_descriptor_extractor.compute_face_descriptor(frame,points)   
            face_descriptor = [f for f in face_descriptor ]
            face_descriptor = np.asarray(face_descriptor,dtype=np.float64)  #将特征转为N维的数组
            # 计算距离
            distance = np.linalg.norm((face_descriptor-feature_list),axis = 1)  #axis = 1  按照行向量进行处理
            # 最小距离索引
            min_index = np.argmin(distance)
            # 最小距离
            min_distance = distance[min_index]  #人脸特征与摄像头所拍摄的特征距离
            predict_id = None
            if min_distance < threshold:
                # 距离小于阈值，表示匹配
                predict_id = label_list[min_index]
                predict_name = name_list[min_index]

                need_insert = False
                now = time.time()
                

                if predict_id not in face_time_dict:
                    face_time_dict[predict_id] = now
                    need_insert = True


                if need_insert and self.recognizedID != predict_id:
                    time_local = time.localtime(face_time_dict[predict_id])
                    #转换成新的时间格式(2016-05-05 20:28:54)
                    face_time = time.strftime("%H:%M:%S",time_local)
                    face_time_full = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                    # 开始位置增加
                    face_info_list.insert(0,[predict_id,face_time])
                    face_img_list.insert( 0, face_crop )
                    # 写入考勤表
                    line = [predict_id,predict_name,min_distance,face_time_full]
                    csv_writer.writerow(line)
                    face_count+=1
                    self.recognizedID = predict_id 
                    
            # Face.recognizedID = predict_id
            # print('====',Face.recognizedID)
        # print(Face.recognizedName)


    def inputFace(self,name,id):
        """
        name: 注册人姓名
        id: 注册人ID
        """
        parser = ArgumentParser()
        parser.add_argument("--mode", type=str, default='reg',
                                    help="运行模式：reg,recog 对应：注册人脸、识别人脸")
        print("进入注册模式")
        parser.add_argument("--id", type=int, default=1,
                    help="人脸ID，正整数不可以重复")
        parser.add_argument("--name", type=str, default='hurn',
                        help="人脸姓名，英文格式")
        parser.add_argument("--interval", type=int, default=3,
                        help="注册人脸每张间隔时间")
        parser.add_argument("--count", type=int, default=3,
                        help="注册人脸照片数量")
        parser.add_argument("--w", type=int, default=0,
                            help="画面缩放宽度")
        parser.add_argument("--h", type=int, default=0,
                            help="画面缩放高度")
        parser.add_argument("--detector", type=str, default='haar',
                        help="人脸识别使用的检测器，可选haar、hog、cnn")
        parser.add_argument("--threshold", type=float, default=0.5,
                            help="人脸识别距离阈值，越低越准确")
        args = parser.parse_args()
        args.id = id #工作编号
        args.name = name #注册人姓名

        self.faceRegiser(faceId=args.id,userName=args.name,interval=args.interval,faceCount=args.count,resize_w=args.w,resize_h=args.h)

    def discernFace(self,image):
        parser = ArgumentParser()
        parser.add_argument("--mode", type=str, default='recog',
                        help="运行模式：reg,recog 对应：注册人脸、识别人脸")
        parser.add_argument("--id", type=int, default=1,
                                        help="人脸ID，正整数不可以重复")
        parser.add_argument("--name", type=str, default='hurn',
                                        help="人脸姓名，英文格式")
        parser.add_argument("--interval", type=int, default=3,
                                        help="注册人脸每张间隔时间")
        parser.add_argument("--count", type=int, default=3,
                                        help="注册人脸照片数量")
        parser.add_argument("--w", type=int, default=0,
                                        help="画面缩放宽度")
        parser.add_argument("--h", type=int, default=0,
                                        help="画面缩放高度")
        parser.add_argument("--detector", type=str, default='haar',
                                        help="人脸识别使用的检测器，可选haar、hog、cnn")
        parser.add_argument("--threshold", type=float, default=0.5,
                                        help="人脸识别距离阈值，越低越准确")
        args = parser.parse_args()
        self.faceRecognize(image,detector=args.detector, threshold=args.threshold)



if __name__ == '__main__':
    face = Face()
    face.inputFace('严婷','513902199711087585')
    # face.discernFace()
