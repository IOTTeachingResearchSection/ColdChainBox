## 安装的库： 

**dlib**  --19.24.0: pip install cmake ; pip install boost ; pip install dlib

**opencv-python**  --4.1.2.30: pip install opencv-python==4.1.2.30

**openvino**  --2021.4.2:  pip install openvino==2021.4.2

**jpype**  --1.3.0: pip install jpype1

**PyQt5** --5.14.1: pip install PyQt5

**PyMySQL**  --1.0.2:  pip install pymysql

**qiniu**  --7.7.1:  pip install qiniu

**baidu-aip** --2.2.17.0:  pip install baidu-aip


## Face：人脸识别

录入人脸：**Face/InputFace.py**  目前人脸录入并未单独封装调用，录入人脸需要运行该代码，并在 main 中填入录入人信息

人脸信息存于：Face/face_data/feature.csv

人脸识别通过后，会存入识别人的信息与时间：Face/face_data/attendance.csv

调用时调用 face 类中的 faceRecognize(image) 方法，image为从视频流中读取到的帧



## Gloves：手套识别

手掌分类器：Gloves/model/palm.xml，model中其余为适用于**openvino**的模型。

使用神经棒时将**self.DEVICE = 'CPU'** 改成**self.DEVICE = 'MYRIAD'** 

 **self.glovesState = None** 记录了当前手套的识别状态。

True：已佩戴手套

False：未佩戴手套

调用时调用Gloves类中的 run(image) 方法，image为从视频流中读取到的帧



## Mask：口罩识别

同手套识别。

口罩识别有三种状态。

**self.recognizeState = None** 记录了当前的识别状态。  

-1:未佩戴口罩，0:未正确佩戴口罩，1：已正确佩戴口罩

调用时调用Mask类中的 run(image) 方法，image为从视频流中读取到的帧



## 上传图片：

将图片上传到图床，主要利用了七牛云的SDK，在**Uploadimg/Uploadimg.py**中



## 识别流程：

整个识别流程在**RecognizeProcess.py**中

人脸识别通过后延时2秒进入口罩，避免人脸识别通过的语音未播报结束，便进入口罩，同样口罩识别成功亦会延时2秒，值的注意的是，这里也必须把口罩佩戴正确超过2秒。

自人脸识别通过后，剩余有效的操作时间为60秒。

切换识别的人脸，需要更改**RecognizeProcess.py** 中初始化函数中的参数 self.targetID = '193080108' 此处还未提供方法进行修改。

每个识别流程通过都会在**recognize_img** 文件夹中生成一个 识别人 ID 的文件夹，其中会保存识别人的每个过程的三张图片。分别为 **face.png**、**mask.png**、**gloves.png**。

整个识别流程为保证不卡顿，语音播报（所有的I/O操作）均采用QT的线程 **QThread** 来实现。

所有的线程操作均在 Thread.py 中。

## 语音播报：

voice 文件夹下保存了所有的语音播报。

**Voice.py** 为调用百度接口生成语音。



## 区块链：

调用了京东开放联盟链网络：[智臻链开放联盟网络](https://openchain.jd.com/)

JDChain/jar中保存着京东区块链的SDK，签名时需要调用其中的方法

请求token，签名，组装交易都已经单独封装在：**JDChain/ContractCall.py，JDChain/GetServerToken.py，JDChain/SignName.py，JDChain/Transaction.py**

修改用户或者智能合约主要对**JDChain/Chain.py** 中的初始化的参数进行修改

**Chain.py** 提供的方法：**insert()** : 插入数据  **updata()** ：更新数据, **query()** ：查询数据

注意：**updata()** 方法更新数据时会将原本插入的数据全部重写。建议先查询原本数据，然后在获取到的字典中写入新加入的数据



## 数据库：

数据库的操作的方法在**MySql/MySql.py**中，主要利用PyMySQL库。

需要修改 **MySQL.py** 中的初始化中的数据库的连接

query() : 查询方法

insert() : 插入数据

updata() : 更新数据



## 运行：

目前直接运行 **MyWindow.py** 即可。

注意：运行前需要修改 **login **方法中**PyMySQL** 的部分。

主要修改：

1.数据库的连接：

conn = pymysql.connect(host='localhost', database='coldboxtest', user='debian-sys-maint', password='VShIsIqvYFvcb5q1', charset='utf8mb4')  

2.sql语句中的表名：

sql = 'SELECT username, password FROM rootuser WHERE username=%s'

注：2可以不做修改，但是需要创建一个名为 rootuser 的表，并存入用户名及信息。