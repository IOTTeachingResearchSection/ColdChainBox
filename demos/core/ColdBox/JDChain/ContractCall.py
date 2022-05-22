import requests
import json
import sys
# from GetServerToken import GetServerToken
# from SignName import SignName

class ContractCall():
    """
    组装交易
    """

    def __init__(self,result:str,didKey:str,didPkPubK:str,publicKey:str,contractAddress:str,method:str,primaryKey:str,paramJson:dict={}) -> None:

        """
        * @param01:result:请求的token
        * @param02:didPkPubK:DID身份信息公钥原文
        * @param03:publicKey:调用合约用的子账户公钥，必须和签名用的子账户私钥是同一对秘钥
        * @param04:contractAddress:合约地址
        * @param05:method：调用方法（insert,query,update,insertOrUpdate四选一）
        * @param06:primaryKey：存证所需的主键。注：存的具体参数，非参数名！
        * @param07:paramJson：存证参数（按照数据格式的dict），调用insert和update方法时需要，query方法不需要
        """

        if result['code'] != 20000:
            print(f'获取Token失败：{result["msg"]}')
            sys.exit(1)
        self.token = result['data']['token']

        #请求头
        self.postHead = {
            'Gateway-Appid': didKey,
            'Gateway-Token': self.token,
        }

        self.postData = {
            'didPkPubK': didPkPubK,
            'subAccountPubKey': publicKey,  # 调用合约用的子账户公钥，必须和签名用的子账户私钥是同一对秘钥
            'contractAddress': contractAddress,
            'method': method,
            'primaryKey': primaryKey,
            'paramJson':  json.dumps(paramJson)
        }


    def postURL(self,url:str='https://openchain.jd.com/server/contract/call') -> dict:
        """
        组装交易后的返回值
        * @param01:url:请求的网址
        """

        page = requests.post(url, headers=self.postHead, json=self.postData) 
        msg = json.loads(page.text)
        return msg

        
# if __name__ == '__main__':

#     didKey = 'ol9iq5T5Eb6HMTl3i9TNGkrJ_QpY'
#     publicKey = '7VeRLfw1QyERTHNZmPJPKwiyyAKFKRDEK9XRsU2L9cL5vf6w'
#     privateKey = '7VeRgVdP6KfF48qQV3BTuhibArrWGxoYYFzZSERwb7Z4D8kr'
#     didPkPubK = '7VeRCSr9WEMrCpW7jqNzp5zg5LSfwvtWpNP4ZguVFgSENneJ' #DID身份信息公钥原文
#     contractAddress = 'LdeP3cRTSHNLpBcacMrH5CTnoVroJES2hAtjH'
#     method = 'insert' #调用方法：insert,query,update,insertOrUpdate四选一
#     paramJson = {#存证参数，调用insert和update方法时需要，query方法不需要
#         "name":"wan"
#     }
#     primaryKey = paramJson['name']  #存证所需的主键
#     signName = SignName(publicKey,privateKey)
#     getServerToken = GetServerToken(publicKey, privateKey, didKey,signName)
#     result = getServerToken.getURl()

#     contractCall = ContractCall(result,didKey,didPkPubK,publicKey,contractAddress,method,primaryKey,paramJson)
#     ans = contractCall.postURL()
#     print(ans)