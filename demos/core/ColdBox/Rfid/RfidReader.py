import serial
import threading
import sys
import cv2
from threading import Timer

PKG_END = 0x7E
PKG_HEADER = 0xBB

TYPE_CMD = 0x00
TYPE_RESP = 0x01
TYPE_INFORM = 0x02

CMD_MULTI_QUERY = 0x22



class RfidReader:
    __alive = False
    cardSet = set()
    
    def __init__(self):
        self.conn = serial.Serial('/dev/ttyUSB0', 115200)
        self.__alive = True
        self.__readThread = threading.Thread(target=self.__readHandler)
        self.__readThread.setDaemon(True)
        self.__readThread.start()

    def put_alive(self):
        print(self.__alive)

    def queryCards(self):
        self.cardSet.clear()
        self.sendMultiQuery()

    def getCardSet(self):
        return set(self.cardSet)

    def sendVerInfo(self):
        """
            查询版本
        """
        self.conn.write(self.__str2hexCmd('BB 00 03 00 01 00 04 7E'))

    def sendMultiQuery(self, cnt=10):
        """
            多次轮训
        """
        strCmd = 'BB 00 27 00 03 22 27 10 83 7E'
        intCmd = [int(sh, 16) for sh in strCmd.split(' ')]
        if cnt != 10000:
            intCmd[6], intCmd[7] = cnt.to_bytes(2, byteorder='big')
            intCmd[8] = self.__checksum(intCmd[1:-2])
        hexCmd = serial.to_bytes(intCmd)
        self.conn.write(hexCmd)

    def killReadHandler(self):
        self.__alive = False

    def aliveReadHandler(self):
        self.__alive = True

    def joinReadThread(self):
        self.__readThread.join()

    def __readHandler(self):
        while self.__alive:

            # 读取包头
            ph = self.conn.read(5) 
            # 读取包数据长度
            pl = int.from_bytes(ph[-2:] , byteorder='big')  
            # 读取包数据
            pd = self.conn.read(pl)
            pc = self.conn.read(1)[0] # 校验位
            pe = self.conn.read(1)[0] # 停止位

            if pe != PKG_END:
                print(f'停止位异常,程序退出, {pe}')
                sys.exit()                

            if not self.__checkChecksum(ph, pd, pc):
                print(f'校验和异常,丢弃包')
                continue

            typ = ph[1]
            cmd = ph[2]
            # print(f'cmd: {hex(cmd)}, typ: {hex(typ)}')
            if typ == TYPE_INFORM and cmd == CMD_MULTI_QUERY:
                epc = pd[3:-2].hex()
                self.cardSet.add(epc[:11])
                # print(f'收到群发通知帧:{epc}')
                
            # verinfo = pd[1:].decode("utf-8") 
            # print(f'verinfo: {verinfo}')
            # break

            

    def __checksum(self, data):
        return sum(data).to_bytes(2, byteorder='big')[-1]

    def __checkChecksum(self, ph, pd, pc):
        return self.__checksum(ph[1:] + pd) == pc

    def __str2hexCmd(self, strCmd):
        return serial.to_bytes([int(sh, 16) for sh in strCmd.split(' ')])

