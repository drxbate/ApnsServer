#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年10月30日

@author: Richard.D
'''

from log import Logger,INFO,DEBUG


class Task:
    __tasks__={}
    def __init__(self,name,log_level=INFO):
        self.logger=Logger.regist("TASK-%s"%name, {"mode":"SYSLOG","name":"TASK-%s"%name,"level":log_level})
        Task.__tasks__[name]=self
        
        
    def __call__(self,func):
        self.__func__=func
    
    def __call_method__(self):
        try:
            self.__func__()
        except:
            self.logger.error("error",exc_info=True)
    

class L(object):
    def __init__(self,name):
        object.__init__(self)
        self.__name__=name
    def __getattribute__(self, key):
        if key in ["debug","error","info","warn","exception"]:
            name = "TASK-%s"%object.__getattribute__(self,"__name__")
            return getattr(Logger.get(name),key)
        else:
            return object.__getattribute__(self,key)
        

def run(name):
    try:
        Task.__tasks__[name].__call_method__()
        L(name).info("success")
    except:
        L(name).error("error",exc_info=True)