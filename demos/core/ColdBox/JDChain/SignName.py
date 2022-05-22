from jpype import *
import jpype
import time

class SignName:
    """
    调用京东提供的SDK，实现本地签名，交易签名
    * @param01: publicKey 公钥原文
    * @param02: privateKey 私钥原文
    
    """
    def __init__(self,publicKey:str,privateKey:str) -> None:
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=/home/pi/Desktop/ColdBox/JDChain/jar/local-signature.jar")  #调用京东区块链的SDK
        self.__JDClass =jpype.JClass("com.jd.bt.chain.Signature") #这说明类在jar包中的目录结构是"com.jd.bt.chain.Signature"  数字签名
        self.__jdChain = self.__JDClass()  #实例化
        self.publicKey = publicKey
        self.privateKey = privateKey

    def localSign(self) -> str:

        """
        返回得到本地签名。
        调用SDK，signOrigin方法
        * @param01: timestamp 时间戳
        * @param02: publicKey 公钥原文
        * @param03: privateKey 私钥原文
        """
        self.timestampContent = str(round(time.time() * 1000))  #毫秒级时间戳
        self.result = str(self.__jdChain.signOrigin(self.timestampContent, self.publicKey,self.privateKey))  #子账户签名结果
        return self.result

    def transactionSign(self,txHash:str) -> str:

        """
        txHash:组装交易后的返回值中。
        返回得到交易签名。
        调用SDK，sign方法
        * @param01: txHash 交易哈希
        * @param02: publicKey 公钥原文
        * @param03: privateKey 私钥原文
        """

        self.result = str(self.__jdChain.sign(txHash, self.publicKey,self.privateKey))  #子账户签名结果
        return self.result
        