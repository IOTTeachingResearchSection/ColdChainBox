from JDChain.GetServerToken import GetServerToken
from JDChain.ContractCall import ContractCall
from JDChain.SignName import SignName
from JDChain.Transaction import Transaction
import json

class Chain:
    def __init__(self) -> None:
        self.didKey = 'ol9iq5T5Eb6HMTl3i9TNGkrJ_QpY'	
        self.publicKey = '7VeRHjup1s9Wizh91qvfdui39DxEzo8W79AysVzrd8aVVTDW'
        self.privateKey = '7VeRdk4TupHDjd4aJWdUnVkj3LbY4Br9v1oXYExJUooAPoDj'
        self.didPkPubK = '7VeRCSr9WEMrCpW7jqNzp5zg5LSfwvtWpNP4ZguVFgSENneJ' 
        self.contractAddress = 'LdeP3RxPBEWsuzRPJ3yH1yLvWbPdWkvCygy5V'
        self.signName = SignName(self.publicKey,self.privateKey)
    
    def insert(self,paramJson):   #插入数据
        method = 'insert'
        primaryKey = paramJson['id']
        getServerToken = GetServerToken(self.publicKey, self.privateKey, self.didKey,self.signName)
        token = getServerToken.getURl()
        contractCall = ContractCall(token,self.didKey,self.didPkPubK,self.publicKey,self.contractAddress,method,primaryKey,paramJson)
        ans = contractCall.postURL()
        transaction = Transaction(ans,contractCall.postHead,self.signName)
        ans = transaction.postURL()
        return json.loads(ans['data']['content'])

    def udpata(self,paramJson): #更新数据
        method = 'update'
        primaryKey = paramJson['id']
        getServerToken = GetServerToken(self.publicKey, self.privateKey, self.didKey,self.signName)
        token = getServerToken.getURl()
        contractCall = ContractCall(token,self.didKey,self.didPkPubK,self.publicKey,self.contractAddress,method,primaryKey,paramJson)
        ans = contractCall.postURL()
        transaction = Transaction(ans,contractCall.postHead,self.signName)
        ans = transaction.postURL()
        return json.loads(ans['data']['content'])

    def query(self,primaryKey):  #查询数据
        method = 'query'
        getServerToken = GetServerToken(self.publicKey, self.privateKey, self.didKey,self.signName)
        token = getServerToken.getURl()
        contractCall = ContractCall(token,self.didKey,self.didPkPubK,self.publicKey,self.contractAddress,method,primaryKey)
        ans = contractCall.postURL()
        transaction = Transaction(ans,contractCall.postHead,self.signName)
        ans = transaction.postURL()
        return ans['data'],json.loads(ans['data']['content'])

# if __name__ == '__main__':
#     chain = Chain()
#     ans = chain.Query('20220505008')
#     print(ans)