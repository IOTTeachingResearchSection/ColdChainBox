import cv2
import numpy as np
from openvino.inference_engine import IECore




class Mask:
    def __init__(self, ie = None) -> None:
        
        self.IR_MODEL_PATH = './Mask/model/ir/saved_model.xml'

        self.haarcascade = cv2.CascadeClassifier('./Mask/model/haarcascade_frontalface_alt.xml')     #把这里改成人脸分类器地址

        #self.DEVICE = 'CPU'
        self.DEVICE = 'MYRIAD' # 神经棒用这个

        if ie is None:
            ie = IECore()
        self.model = ie.read_network(self.IR_MODEL_PATH)
        self.input_blob = next(iter(self.model.input_info))
        self.out_blob = next(iter(self.model.outputs))
        self.model.input_info[self.input_blob].precision = 'U8'
        self.model.outputs[self.out_blob].precision = 'FP16'
        self.num_of_classes = max(self.model.outputs[self.out_blob].shape)
        self.exec_net = ie.load_network(network=self.model, device_name=self.DEVICE)
        
        self.recognizeState = None
        self.rect_size = 5

        self.__sw = []
        self.__swTop = True
        self.__swLen = 20
        self.__swdis = self.__swLen//10

    
    def run(self,image):

        (h, w) = image.shape[:2]
        rerect_size = cv2.resize(image, (w // self.rect_size, h //self.rect_size))
        haarfaces = self.haarcascade.detectMultiScale(rerect_size )
        locs = []
        faces = []
        for f in haarfaces:
            (x, y, w, h) = [v * self.rect_size for v in f]
            startX, startY, endX, endY = x, y, x+w, y+h

            face = image[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))

            faces.append(face)
            locs.append((startX, startY, endX, endY))

        for face in faces:
            # face = cv2.resize(face, (224, 224))
            face = face.transpose((2, 0, 1))
            face = np.expand_dims(face, axis=0)
            res = self.exec_net.infer(inputs={self.input_blob: face})
            res = res[self.out_blob]
            probs = res.reshape(self.num_of_classes)

            if self.__swTop:
                self.__sw.append(probs[0])
                if len(self.__sw) == self.__swLen:
                    self.__swTop = False
                avgPro = sum(self.__sw)/len(self.__sw)
                
            else:
                self.__sw = self.__sw[1:]
                self.__sw.append(probs[0])

                swc = self.__sw[::]
                swc.sort()
                print(swc)
                avgPro = (sum(swc[self.__swdis:(self.__swLen - self.__swdis-1)]))/(self.__swLen - self.__swdis*2)
                # avgPro = (sum(self.__sw) - self.__maxPro - self.__minPro)/18
            print(self.__sw)
            print(len(self.__sw))
            #print(avgPro)

        if len(faces) > 0:
            startX, startY, endX, endY = locs[0]

            if avgPro > 0.70:
                label = 'Mask worn'
                color = (0, 255, 0)
                self.recognizeState = 1
            elif avgPro > 0.40:
                color = (0,255,255)
                label = 'Please wear masks in a standard way'
                self.recognizeState = 0
            else:
                label = 'Please wear a mask'
                color = (0,0,255)
                self.recognizeState = -1

            cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
            cv2.putText(image, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        
        else:
            self.__swTop = True
            self.__sw = []

                
if __name__ == '__main__':
    faces = Mask()
    cap = cv2.VideoCapture(0)
    while True:
        image = cap.read()[1]
        faces.run(image)
        cv2.imshow('test',image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
