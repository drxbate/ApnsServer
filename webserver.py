#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014-2-14

@author: Rich
'''
 
from flask import Flask, g, request,Response

import json


from libs.log import Logger
from libs.cache import Cache,get_incr,reset_incr
from libs import const
from MSMQ import ApnsMQ

app = Flask(__name__)
app.debug = True

logger=Logger.regist("httpd","WWW", {"mode":"SYSLOG","name":"WWW","level":Logger.DEBUG})

def incTokenCounter(token,value=1):
    return get_incr("TOKEN:"%token, value)

def resetTokenCount(token):
    reset_incr("TOKEN:"%token)

@app.route("/state",methods=["GET"])
def root():
    return "running...."

@app.route("/message/put",methods=["GET","POST"])
def putMessage(): 
    try:        
        tokens,message=request.form["tokens"],request.form["message"]
        if message=='!:reset':
            for token in tokens.split(","):
                resetTokenCount(token)
            return json.dumps({"state":0,"result":"ok"})
                
        try:
            ex=json.loads(request.form["ex"])
        except:
            ex={}
            pass
        
        if len(tokens)!=64:
            logger.debug("invalid token")
            return json.dumps({"state":-1,"result":"invalid token"})
        
        if len(message)==0:
            logger.debug("invalid message")
            return json.dumps({"state":-1,"result":"invalid message"})
        
        
        badge=0
        try:
            badge=int(request.form["badge"])
        except:
            pass
        
        cert=""
        try:
            cert=request.form["cert"]
        except:
            pass
        
        logger.info("/message/put %s %s %s",tokens,message,cert)
        
        if len(message)>=100:
            message=message[0:100]
            logger.debug("sub-message %s %s",tokens,message)
        

        
        
        for token in tokens.split(const.TOKENS_SPLIT_STR):
            badge = incTokenCounter(token,badge)
            
            payload=json.dumps({"aps":{"alert":message,"badge":badge,"sound":"default","content-available":1},"ecmc":ex})                
            ApnsMQ.enter(token, payload, {"cert":cert})
            
        return json.dumps({"state":0,"result":"ok"})
    except Exception,e:
        import traceback
        logger.exception("/message/put %s",traceback.format_stack())
        return json.dumps({"state":-1,"result":str(e)})
    
@app.route("/message/putList",methods=["GET","POST"])
def putMessageCollection(): 
    try:
        logger.debug("putMessageCollection")        
        ps = json.loads(request.form["packages"])
        cert = request.forms.get("cert")
        logger.debug(ps)
        for i in ps:
            token,message=i["token"],i["message"]
            
            try:
                ex=json.loads(i["ex"])
            except:
                ex={}
                pass
            
            if len(token)!=64:
                logger.debug("invalid token")
                continue
            
            if len(message)==0:
                logger.debug("invalid message")
                continue
            
            badge=1
            try:
                badge=int(i["badge"])
            except:
                pass
            badge = incTokenCounter(token,badge)

            
            logger.info("/message/putCollection-One %s %s",token,message)
            
            if len(message)>=100:
                message=message[0:100]
                logger.debug("sub-message %s %s",token,message)
            
            
            payload=json.dumps({"aps":{"alert":message,"badge":badge,"sound":"default","content-available":1},"ecmc":ex})
            
            ApnsMQ.enter(token, payload.encode("utf8"), opts=dict(cert=cert))

        
        return json.dumps({"state":0,"result":"ok"})
    except Exception,e:
        logger.exception("/message/put")
        return json.dumps({"state":-1,"result":str(e)})
        
@app.route("/message/resetCounter",methods=["GET","POST"])
def resetCounter():
    token=request.form["token"]
    resetTokenCount(token,0)
    return json.dumps({"state":0,"result":"ok"})

def run():
    print "run httpd"
    app.run(host="0.0.0.0",port=9910,debug=True)
    

if __name__=="__main__":
    run()