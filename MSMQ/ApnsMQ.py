#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年6月3日
@author: ruixidong
'''
from MessageQueue import MSMQ
import libs.const as const

NAME="APNS_MESSAGE_QUEUE"


def restore():
    MSMQ(NAME).restore()

def enter(token,payload,opts={},priority=3):
    MSMQ(NAME).enter(dict(token=token,payload=payload,opts=opts), priority)

def fetch(amount=10):
    l = MSMQ(NAME).__fetch__(amount,discard=True)
    for _id,data in l:
        yield (data["token"],data["payload"],data["opts"])