import requests
import json

# from GetServerToken import GetServerToken
# from ContractCall import ContractCall
# from SignName import SignName

class Transaction:
    """
    交易
    """
    def __init__(self,result:dict,postHead,signName) -> None:

        """
        * @param01: result 组装交易后的返回值
        * @param02:SignName:签名类的实例化
        """

        self.postHead = postHead
        self.data = result['data']
        self.txHash = result['data']['txHash']
        self.signName = signName
        self.signerPubKey = self.signName.transactionSign(self.txHash)
        self.data['signature'] = self.signerPubKey

    def postURL(self,url='https://openchain.jd.com/server/contract/sign') -> dict:
        """
        最终交易后的返回值
        * @param01:url:请求的网址
        """
        
        page = requests.post(url, headers=self.postHead,json=self.data) 
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
#         "name":"young"
#     }
#     signName = SignName(publicKey,privateKey)
#     primaryKey = paramJson['name']  #存证所需的主键
#     getServerToken = GetServerToken(publicKey, privateKey, didKey,signName)
#     result = getServerToken.getURl()

#     contractCall = ContractCall(result,didKey,didPkPubK,publicKey,contractAddress,method,primaryKey,paramJson)
#     ans = contractCall.postURL()
#     transaction = Transaction(ans,contractCall.postHead,signName)
#     ans = transaction.postURL()
#     print(ans)
