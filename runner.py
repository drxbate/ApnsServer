#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年10月30日

@author: Richard.D
'''
import sys,os

reload(sys)
setdefaultencoding = getattr(sys, "setdefaultencoding")
if setdefaultencoding:
    setdefaultencoding("utf8") 


from libs import task, daemon
from Services import apns

def main(*argv):
    name,state="",""
    if len(argv)>=1:
        name=argv[0]
        state=argv[1] if len(argv)==2 else None
    else:
        name=sys.argv[1]
        state=sys.argv[2] if len(sys.argv)==3 else None
    
    if state!=None:
        daemon.process(name,state)
    else:
        task.run(name)
    
if __name__=="__main__":
    main()
 
