#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014-8-2

@author: Rich
'''


"""
class Protocal(object):
    def connect(self):
        pass
    def write(self,msg):
        pass
    def read(self):
        pass
    def keepalive(self): 
        pass
"""

from libs import const

import time,json,ssl,socket

from libs.MessageCollection import MessageCollection
from libs.daemon import Daemon
from MSMQ import ApnsMQ
from libs.MultiProcess import Worker

from libs.log import Logger

logger=Logger.get("protocol")
logger_fb=Logger.get("feedback")
logger_app=Logger.get()

PROTOCAL_MODEL = const.RELEASE
APNS_HOST = (const.APNS_SANDBOX_HOST 
             if PROTOCAL_MODEL==const.DEBUG
             else const.APNS_HOST)

FB_HOST = (const.FB_SANDBOX_HOST 
             if PROTOCAL_MODEL==const.DEBUG
             else const.FB_HOST)

CERT_FILE = (const.CERT_FILE_SANDBOX 
             if PROTOCAL_MODEL==const.DEBUG
             else const.CERT_FILE)


"""
发送打包数据
完成后，调用feedback
"""            

""" 
MESSAGE_QUEUE=[MESSAGE_0,MESSAGE_1,....]
"""


#print(id(MESSAGE_IDLE_QUEUE),id(MESSAGE_ING_POOL),id(DEVICES))


@Daemon("APNS_PROCESSOR_FEEDBACK")
def feedback():
    import select
    logger_fb.debug("FB_HOST: %s",FB_HOST)
    while True:
        try:
            client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(FB_HOST)
            #client.setblocking(False)
            client=ssl.wrap_socket(client, certfile='my.pem')
            #client.connect(FB_HOST)
            
            while True:
                try:
                    client.do_handshake()
                    break
                except ssl.SSLError, err:
                    if ssl.SSL_ERROR_WANT_READ == err.args[0]:
                        select.select([client], [], [])
                    elif ssl.SSL_ERROR_WANT_WRITE == err.args[0]:
                        select.select([], [client], [])
                    else:
                        raise
                else:
                    logger.exception()
            while True:
                data = client.read(38)
                if len(data)>0:                        
                    logger_fb.info("Feedback::%s","{0}".format(str(list(data))))

                if len(data)==0:
                    break
        except:
            logger.exception()
        
        client.close
        time.sleep(5)
            

        


@Daemon("APNS_PROCESSOR_POLL")
def poll():
    def _poll():
                
        #__queue_ing__ = StorageSpace.getMessageIngPool()        

        colls =  {}
        
        for token,payload,opts in ApnsMQ.fetch(100):
            k=json.dumps(opts)
            if not colls.has_key(k):
                colls[k]=MessageCollection()
            colls[k].enter(dict(token=token,payload=payload,opts=opts))
            
        for k,coll in colls.items():
            opts=json.loads(k)
            sendmessage(coll, opts)                
            #msg.process(self.sendmessage,self.callback)
    while True:
        try:
            _poll()
        except:
            pass
        time.sleep(0.01)

def get_connection(cert,reconn=False):
    if not hasattr(get_connection, "__conn_pool__"):
        get_connection.__conn_pool__={}
        
    if not get_connection.__conn_pool__.has_key(cert):
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client=ssl.wrap_socket(client,ssl_version=ssl.PROTOCOL_SSLv3, certfile=cert)
        get_connection.__conn_pool__[cert]=client
        
    if reconn:
        client.close()
        client.connect(APNS_HOST)
        
    return get_connection.__conn_pool__[cert]

@Worker("APNS_MESSAGE_SENDER",workers=10)
def sendmessage(coll,opts):    
    client=None
    cert = CERT_FILE if not opts.has_key("cert") or opts["cert"]=="" else opts["cert"]
    
    logger.debug("cert-file %s",cert)
    
    try:
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client=ssl.wrap_socket(client, certfile='my.pem')
        client.connect(APNS_HOST)
        coll.write(client)

        
        
        logger.info("send data %d",len(bytes))
        
        client.settimeout(5)
        data = None
        try:
            data = client.recv()
            if len(data)>0:
                logger.info("read data complete %d",len(data))
        except ssl.SSLError,ex:
            if ex.message=="The read operation timed out":
                logger.warn("The read operation timed out")
            else:                
                logger.exception()
        except Exception:
            logger.exception()
        finally:
            return data
    except Exception,e:
        logger.exception()
    finally:
        if client:          
            client.close()



        
    
