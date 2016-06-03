#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014-2-14

@author: Rich
'''

import os
import const,convert,ctypes,threading,struct
import base64
from array import array
from log import Logger

logger=Logger.get("apns")

class MessageCollection(dict):
    def enter(self,message):
        self[message["nid"]] = message
    
   
    def write(self,output):
        
        buff=""
                
        for nid,m in self.items():
            
            bb=BufferBuilder()
            #command
            bb.append(2)
            #command framelength
            bb.append(0,4)
            
            #1 token
            bb.append(1)
            bb.append(32,2)
            bb.append(m["token"].decode("hex"),32)
    
            #2 token
            bb.append(2)
            bb.append(len(m["payload"]),2)
            bb.append(m["payload"])
            
            #3 Notification identifier
            bb.append(3)
            bb.append(4,2)
            bb.append(nid,4)
    
            #4 Expiration date
            bb.append(4)
            bb.append(4,2)
            bb.append(0,4)
    
            #4 Expiration date
            bb.append(5)
            bb.append(1,2)
            bb.append(10)                                    
            ##set length
            bb.set(1,bb.getsize()-5,4)
            buff+= bb.getbytes()
            
        output.write(buff)

            
    def callback(self,data,callback):
        
        if data!=None:
            for i in range(0,len(data)/6):
                base=i*6
                _data=data[0+base:6]
                
                _data = list(array('b',_data))
                err = _data[1+base] 
    
                err = const.ERROR_MESSAGES[err]
                
                buff=bytearray(_data[2+base:6+base])
                nid = struct.unpack(">I",buff)[0]
                if nid>0:
                    logger.error("SEND error(%s) %d %s %s",err,nid,self[nid]["token"],self[nid]["payload"])
                else:
                    logger.error("SEND error %s",err)
        callback("OVR",self)
            
    def __cmp__(self,other):
        return self.__id__==other.__id__

def __getbytes__(data,size=0):
    if type(data)==long or type(data)==int:
        bytes = bytearray(convert.long_to_bytes(data, size=size))
    else:
        bytes = bytearray(data)
    #bytes.reverse()
    return bytes

class BufferBuilder(list):
    def __init__(self):
        list.__init__(self)
        self.__size__ = 0

            
    def getsize(self):
        return self.__size__
    def append(self,data,size=0):
        bytes=__getbytes__(data,size)
        self.__size__+=len(bytes)
        list.append(self,bytes)
    def insert(self,index,data,size=0):
        bytes=__getbytes__(data,size)
        self.__size__+=len(bytes)
        list.insert(self,index, bytes)
        
    def getbytes(self):
        bytes=bytearray()
        [bytes.extend(x) for x in self]
        #bytes.reverse()
        return bytes
    
    def set(self,index,data,size=0):
        bytes = __getbytes__(data,size)
        self[index] = bytearray(bytes)