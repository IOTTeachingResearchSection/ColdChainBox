import requests
import json
# from SignName import SignName

class GetServerToken:
    """
    token请求类
    """
    def __init__(self,publicKey:str,privateKey:str,didKey:str,signName) -> None:

        """
        * @param01:publicKey：子账户公钥
        * @param02:privateKey：子账户密钥
        * @param03:didKey:账户
        * @param04:SignName:签名类的实例化
        """
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.didKey = didKey
        self.signName = signName


    def getURl(self,url='https://openchain.jd.com/server/account/getServerToken') -> dict:
        """
        请求的token
        * @param01:url:请求的网址
        """

        param = {
            'didKey':self.didKey,
            'subAccountPubKey':self.publicKey,
            'signature':self.signName.localSign(),   #子账户签名结果
            'timestamp':self.signName.timestampContent   #时间戳（被签名内容）
        }
        page = requests.get(url,params=param)
        msg = json.loads(page.text)
        return msg


# if __name__ == '__main__':
#     didKey = 'ol9iq5T5Eb6HMTl3i9TNGkrJ_QpY'
#     publicKey = '7VeRLfw1QyERTHNZmPJPKwiyyAKFKRDEK9XRsU2L9cL5vf6w'
#     privateKey = '7VeRgVdP6KfF48qQV3BTuhibArrWGxoYYFzZSERwb7Z4D8kr'
    
#     signName = SignName(publicKey,privateKey)
#     print(type(signName))
#     askToken = GetServerToken(publicKey,privateKey,didKey,signName)
#     msg = askToken.getURl()

#     print(msg)




