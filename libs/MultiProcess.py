#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
守护进程定义

定义守护进程
@daemon.Daemon("TaskDaemon")
def run():
    TaskModules.run_tasks()
    while True:
        time.sleep(100)
        
启动守护进程
daemon.process() 执行所有进程
daemon.process("TaskDaemon") 执行指定进程
"""

import sys, os, time, atexit
from signal import SIGTERM 
from os.path import exists
import functools
from multiprocessing import Pool

WOARK_PATH=os.getcwd()

__multi_process_pools__={}

def Worker(name,workers=None,callback=None):
    if not __multi_process_pools__.has_key(name):
        __multi_process_pools__[name]=Pool(workers)
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            res = __multi_process_pools__[name].apply_async(func,args,kwargs,callback)
            callback!=None and callback(res)
        return inner
    return wrapper