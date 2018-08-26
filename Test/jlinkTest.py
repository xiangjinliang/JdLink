#!/usr/bin/env python   
# -*- coding:UTF-8 -*-  
from socket import *  
import time  
import json

def writeFileToLocal(strDat,filePath,rPro):
    f=open(filePath,str(rPro))
    f.write(strDat)  
    f.close()  
    
def createTestProcess(subDevIp,subDevPort):
    print("create sub process,ip(%s,%d)"%(subDevIp,subDevPort))
    
def parseJdLinkMsg(jstr):
    print('parse jdlink json:\n')
    #解析json数据串
    jdindex = jstr.find("{")
    jdAdstr = jstr[jdindex:len(jstr)-1]
    #替换字符串中不需要的特殊字符
    jdAdstr=jdAdstr.replace('\\t','')
    jdAdstr=jdAdstr.replace('\\n','')
    print(jdAdstr)
    writeFileToLocal(jdAdstr,"recJson.json", "w")

    #json 字符串
    jdJson=json.loads(jdAdstr)
    print("sv_name:"+jdJson['sv_name'])
    print("sig_name:"+jdJson['sig_name'])         
    print("complete json info:\n %s"%jdJson)  
    if 'announce' == jdJson['sig_name']:
        return 1
    else:
        print("this is not announce infomation.")
        return 0

#接收广播消息
def recBroadCast():
    HOST = '127.0.0.1'  
    PORT = 30002  
    BUFSIZE = 1024  
    ADDR = (HOST,PORT)  
    udpSerSock = socket(AF_INET, SOCK_DGRAM)
    #设置阻塞
    udpSerSock.setblocking(1)
    #设置超时时间 8s
    udpSerSock.settimeout(10)  
    udpSerSock.bind(('',PORT))
    udpSerSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) 
    index = 0
    while True:  
        try: 
            data, addr = udpSerSock.recvfrom(BUFSIZE)  
            curtime = time.time()  # 获取当前时间戳
            time_str = time.ctime(curtime)  # 转为string格式
            print('\nReceived message(indx:%d,Time:%s) from %s >> %s' % (index,time_str,addr, data))            
            writeFileToLocal(data,"recJsonOrigin.txt","wb+")
            if data:
                jstr = str(data)
                isCommAbout = jstr.find("com.joylink.about")##广播消息判断
                if isCommAbout < 0:
                    print("pass: not jdlink infomation,break.flag(%)"%isCommAbout)
                    pass
                
                if parseJdLinkMsg(jstr) == 1:
                    createTestProcess(addr[0],addr[1])              
                index = index+1
        except Exception as err:
            print(err) 
    udpSerSock.close()
#代码执行入口处
if __name__ == "__main__":
    print("jdLink Test process..")
    recBroadCast()