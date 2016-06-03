#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年1月20日

@author: Richard.D
'''
REDIS_ROOT="WECHATCOR"
REDIS_CACHE="%s:CACHE"%REDIS_ROOT
REDIS_MSMQ="%s:MSMQ"%REDIS_ROOT
REDIS_DEVICE_LIST="%s:DEVICE_LIST"%REDIS_ROOT
REDIS_DEVICE_ADDRESS_LIST="%s:DEVICE_ADDRESS_LIST"%REDIS_ROOT
REDIS_METADATA="%s:REDIS_METADATA"%REDIS_ROOT
REDIS_USER_CODE="%s:USER_CODE"%REDIS_ROOT
REDIS_IMPERSONATION="%s:IMPERSONATION"%REDIS_ROOT
REDIS_SESSION_INFO="%s:SESSION_INFO"%REDIS_ROOT
REDIS_FUNC="%s:FUNC"%REDIS_ROOT
REDIS_CHECKPOINT_STATE="%s:CHECKPOINT_STATE"%REDIS_ROOT
REDIS_CHECKPOINT_OPTION="%s:CHECKPOINT_OPTION"%REDIS_ROOT
REDIS_DOCUMENTS="%s:DOCUMENTS"%REDIS_ROOT
REDIS_DOCUMENTS_INCR="%s:DOCUMENTS_INCR"%REDIS_ROOT
REDIS_DOCUMENTS_INDEX="%s:DOCUMENTS_INDEX"%REDIS_ROOT
REDIS_DOCUMENTS_RECYCLE_BIN="%s:DOCUMENTS_RECYCLE_BIN"%REDIS_ROOT
CACHE_ACCESS_TOKEN="accessToken"
CACHE_JSAPI_TICKET="jsapi_ticket"
CACHE_ETL_DUTY_LAST_TIME="etl_duty_ltime" #存放上次计算考勤时间
CACHE_ETL_LOCK="etl_lock"
CACHE_ALARM_CONTENT="CACHE_ALARM_CONTENT"



SS_SERVICE_ADDRESS = ("localhost",6003) 
HTTP_SERVICE_ADDRESS = ("0.0.0.0",6001)


RELEASE = "RELEASE"
DEBUG = "DEBUG"


APNS_SANDBOX_HOST = ("gateway.sandbox.push.apple.com",2195)
APNS_HOST = ("gateway.push.apple.com",2195)

FB_SANDBOX_HOST = ("feedback.sandbox.push.apple.com",2196)
FB_HOST = ("feedback.push.apple.com",2196)

CERT_FILE_SANDBOX="my-sanbox.pem"
CERT_FILE="my.pem"

NotificationIdentifier = "NotificationIdentifier"

SERVICE=""
STORAGE_SPACE_SERVICE="STORAGE_SPACE_SERVICE"
WEB_SERVICE="WEB_SERVICE"
PROTOCOL_SERVICE="PROTOCOL_SERVICE"

class classproperty(object):

    def __init__(self, getter
            #, setter
        ):
        self.getter = getter
    #    self.setter = setter

    def __get__(self, instance, owner):
        return self.getter(owner)
    
ERROR_MESSAGES = {0:"No errors encountered",
                  1:"Processing error",
                  2:"Missing device token",
                  3:"Missing topic",
                  4:"Missing payload",
                  5:"Invalid token size",
                  6:"Invalid topic size",
                  7:"Invalid payload size",
                  8:"Invalid token",
                  10:"Shutdown",
                  255:"None (unknown)",
                  }
TOKENS_SPLIT_STR="\n------*--------token--split---------*--------\n"

MAX_THREADS_SIZE = 10

LOG_FEEDBACK="FEEDBACK"
LID_FEEDBACK=60
