#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年3月13日

@author: Richard.D
'''

from redis import Redis


from libs.log import Logger
from libs.setting import Settings
from sys import exc_info
import json
from libs.const import REDIS_ROOT,REDIS_CACHE,REDIS_MSMQ,REDIS_DEVICE_LIST, \
                REDIS_DEVICE_ADDRESS_LIST,REDIS_METADATA,REDIS_USER_CODE,REDIS_IMPERSONATION,\
                REDIS_SESSION_INFO,REDIS_FUNC,REDIS_DOCUMENTS,REDIS_DOCUMENTS_INCR,REDIS_DOCUMENTS_INDEX,REDIS_DOCUMENTS_RECYCLE_BIN,\
                REDIS_CHECKPOINT_STATE,REDIS_CHECKPOINT_OPTION,\
                CACHE_ACCESS_TOKEN,CACHE_JSAPI_TICKET,CACHE_ETL_DUTY_LAST_TIME,CACHE_ETL_LOCK,CACHE_ALARM_CONTENT
import functools




L=Logger.regist("cache", {"file":"cache","level":Logger.DEBUG})

class __RedisHandler__(Redis):
    def __init__(self):
        Redis.__init__(self,host=Settings.Redis.Host,port=6379)

RedisCli=__RedisHandler__()



class __cache__(dict):
    def __getitem__(self, key):
        return RedisCli.hget(REDIS_CACHE, key)
    def __setitem__(self, key,value):
        RedisCli.hset(REDIS_CACHE, key, value)

Cache=__cache__()

def get_incr(name,value=1):
    return RedisCli.execute_command("incrby","%s:incr:%s"%(REDIS_ROOT,name),value)
def reset_incr(name):
    RedisCli.delete("%s:incr:%s"%(REDIS_ROOT,name))

def cached(name,ex):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            res=RedisCli.get("%s:%s"%(REDIS_FUNC,name))
            if res==None:
                res = func(*args,**kwargs)
                if res!=None:
                    RedisCli.set("%s:%s"%(REDIS_FUNC,name),json.dumps(res),ex=ex)
                return res
            else:
                return json.loads(res)
        return inner
    return wrapper

