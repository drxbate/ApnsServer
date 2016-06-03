#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年1月19日

@author: Richard.D
'''
import sys
sys.path.append("..")

from libs.cache import RedisCli
import json
from libs.log import Logger
from libs.const import REDIS_MSMQ 
from multiprocessing import Pool

L=Logger.regist("MessageQueue", {"file":"MessageQueue","level":Logger.DEBUG})

class MSMQ:
    
    MSMQ_REG_TEMP_ACCOUNT="TEMP_ACCOUNT" #Data-Format:dict(name='张xx',dept='57001xy',cellphone='130xxxxxx0',operator='570014081') 
    
    MSMQ_CHECK_POINT="CHECK_POINT" #Data-Format:dict(dev=dev,code=code,ts=int(ts))
    MSMQ_OUTBOX_TEXT="OUTBOX_TEXT"
    MSMQ_OUTBOX_NEWS="OUTBOX_NEWS"
    MSMQ_EVENT="EVENTS"
    
    def __init__(self,type):
        self.type=type
        self.__rname__="%s:%s"%(REDIS_MSMQ,self.type)
    def enter(self,data,priority=5):
        '''
        priority=0~5,0:System,1:Highest,5:Lowest
        '''
        RedisCli.rpush("%s:%d"%(self.__rname__,priority),json.dumps(data))
    def ___fetch__(self,amount=1,discard=False):
        '''
        DISCARD aft. fetched. else data will be persisted。Default No DISCARD
        '''
        lname = "%s:T"%self.__rname__
        inc_key = "%s:_inc"%self.__rname__
        l=[]
        for priority in range(0,6):
            qname="%s:%d"%(self.__rname__,priority)
            while RedisCli.llen(qname)>0:
                v = RedisCli.lpop(qname)
                _id=RedisCli.incr(inc_key)
                if discard==False:
                    RedisCli.hset(lname,_id,v)
                l.append((_id,v))
                if len(l)>=amount:
                    return l
        return l
        
    def fetch(self,func=None,async=False):
        '''
        func:=func(data)
        Drop item as NONE-FUNC or func returns False
        Returns True when anything else in the MSMQ
        ALWAYS Returns None as async=False
        '''

                
        __callable__=__proccess_callable__(self.__rname__,func)
        if async==False:
            try:
                for _id,v in self.___fetch__(amount=1):                    
                    obj=json.loads(v)
                    __callable__(_id,obj)
                    
            except:
                L.error("Process MSMQ(%s) Error\n%s\n"%(self.type,v),exc_info=True)
            return sum([RedisCli.llen("%s:%d"%(self.__rname__,priority)) for priority in range(0,6)])>0
        else:
            ll=[]
            pool=Pool(10)
            for _id,v in self.___fetch__(amount=10):
                try:
                    obj = json.loads(v)

                    result = pool.apply_async(
                                     __callable__,
                                     args=(_id,obj)
                                     )
                except Exception,e:
                    pass
            pool.close()
            pool.join()
            
            
        
    def restore(self):
        lname = "%s:T"%self.__rname__
        d = RedisCli.hgetall(lname)
        for k,v in d.items():
            self.enter(json.loads(v), 0)
            RedisCli.hdel(lname,k)

class __proccess_callable__:
    def __init__(self,msmq_name,callable):
        self.msmq_name=msmq_name
        self.__callable__=callable
    def __call__(self,_id,obj):
        if self.__callable__(obj):
            lname = "%s:T"%self.msmq_name
            RedisCli.hdel(lname,_id)