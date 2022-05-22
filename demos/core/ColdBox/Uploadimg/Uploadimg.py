import uuid
from qiniu import Auth, put_file

class Uploadimg:
    def __init__(self,ak='eI32XLN-L0SSrdHBb2Na0JOKQCbQbpf8M2Hp22kc',sk='z-xW2wT4Tb5ErUzrEVP7Ei6S2jSR4EQRIv1b8ser') -> None:
        self.access_key = ak
        self.secret_key = sk


    # 生成上传凭证
    def qiniu_token(self,bucked_name, key):
        q = Auth(access_key=self.access_key,
                secret_key=self.secret_key)
        token = q.upload_token(bucked_name, key)
        return token


    def upload_img(self,file_path):
        """
        收集本地信息到云服务器上
        参考地址：https://developer.qiniu.com/kodo/sdk/1242/python
        """
        bucked_name = 'wyoung'
        # 指定图片名称,上传后保存的文件名
        file_name = '{}.png'.format(uuid.uuid4())
        # 指定上传空间，获取token
        token = self.qiniu_token(bucked_name, file_name)

        # file_path = '/home/ubuntu/Desktop/demo.png'
        ret, info = put_file(token, file_name, file_path)

        img_key = ret.get('key')
        return 'http://rbyqbxn2g.hn-bkt.clouddn.com/' + img_key

if __name__ == '__main__':
    path = ['/home/young/桌面/001/ColdBox/recognize_img/203080040/face.png','/home/young/桌面/001/ColdBox/recognize_img/203080040/mask.png','/home/young/桌面/001/ColdBox/recognize_img/203080040/gloves.png']
    q = Uploadimg()
    for i in path:
        a = q.upload_img(i)
        print(a)
    # print(len('http://rbcnabcld.hn-bkt.clouddn.com/359874b5-9e4c-426d-9d4e-02190498e478.jpge'))