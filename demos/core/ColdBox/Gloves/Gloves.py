import cv2
import numpy as np
from openvino.inference_engine import IECore




class Gloves:
    def __init__(self, ie = None) -> None:
        
        self.IR_MODEL_PATH = './Gloves/model/ir/saved_model.xml'
        self.haarcascade = cv2.CascadeClassifier('./Gloves/model/palm.xml')
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
        self.glovesState = None
        self.rect_size = 5

    
    def run(self,image):

        (h, w) = image.shape[:2]
        rerect_size = cv2.resize(image, (w // self.rect_size, h //self.rect_size))
        haargloves = self.haarcascade.detectMultiScale(rerect_size )
        locs = []
        gloves = []
        for f in haargloves:
            (x, y, w, h) = [v * self.rect_size for v in f]
            startX, startY, endX, endY = x, y, x+w, y+h

            face = image[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))

            gloves.append(face)
            locs.append((startX, startY, endX, endY))

        for glove in gloves:
            # glove = cv2.resize(glove, (224, 224))
            glove = glove.transpose((2, 0, 1))
            glove = np.expand_dims(glove, axis=0)
            res = self.exec_net.infer(inputs={self.input_blob: glove})
            res = res[self.out_blob]
            probs = res.reshape(self.num_of_classes)
            top_n_idexes = np.argsort(probs)[-2:][::-1]
            # print('top_n_idexes:',top_n_idexes)
            # print('probs: %.7f %.7f'%(probs[top_n_idexes[0]],probs[top_n_idexes[1]]))


        if len(gloves) > 0:

            top = list(top_n_idexes)
            if top[0] == 0:
                label = 'Gloves worn'
                color = (0, 255, 0)
                self.glovesState = True 
            else:
                label = 'Please wear gloves'
                color = (0, 0, 255)
                self.glovesState = False
            cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
            cv2.putText(image, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)


        
if __name__ == '__main__':
    gloves = Gloves()
    cap = cv2.VideoCapture(0)
    while True:
        image = cap.read()[1]
        gloves.run(image)
        cv2.imshow('test',image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
