#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年9月15日

@author: ruixidong

** e.g. 从配置文件中获取数据
value=Settings.header.key

** File 'setting' **
[header]
key=value

'''

import ConfigParser,os


class __config__:
    options={"configFile":"%s/setting"%os.getcwd()}
    @classmethod
    def setOptions(cls,options):
        cls.options.update(options)
        cls.refresh()
    @classmethod
    def get_parser(cls):
        if not hasattr(cls,"__parser__"):
            cls.__parser__ = ConfigParser.SafeConfigParser()
            
            cls.__parser__.read(cls.options["configFile"])
        return cls.__parser__ 
    @classmethod
    def refresh(cls):
        p = cls.get_parser()
        p.read(cls.options["configFile"])
        return p
    @classmethod
    def update(cls,dict):
        '''
        {
        sections:{option:value,option,value...}
        ...
        }
        '''
        p=__config__.get_parser()
        for s,options in dict.items():
            if not p.has_section(s):
                p.add_section(s)
            for opt,val in options.items():
                p.set(s,opt,val)
        p.write(open(cls.options["configFile"],"w"))

class _options(dict):
    def __init__(self,section):
        self.section=section
        self.conf=__config__.get_parser()
    def get(self, opt):
        if dict.has_key(self,opt):
            return dict.get(self, opt)
        else:
            val=self.conf.get(self.section,opt)
            dict.update(self,{opt:val})
            return val
    def __getattribute__(self, key):
        if dict.__getattribute__(self,"conf").has_option(dict.__getattribute__(self, "section"), key):
            return self.get(key)
        else:
            return dict.__getattribute__(self, key)
    
class _Settings(dict):
    def __init__(self):
        self.conf=__config__.get_parser()
    def get(self, key):
        if dict.has_key(self,key):
            return dict.get(self, key)
        else:
            option=_options(key)
            dict.update(self,{key:option})
            return option
    def save(self):
        __config__.update(self)
    def refresh(self):
        self.clear()
        __config__.refresh()
    def __getattribute__(self, key):
        if dict.__getattribute__(self,"conf").has_section(key):
            return self.get(key)
        else:
            return dict.__getattribute__(self,key)
    def setOptions(self,**options):
        __config__.setOptions(options)
    def has_key(self, section):
        return self.conf.has_section(section)
    def has_option(self, section, option):
        return self.conf.has_option(section, option)
Settings = _Settings()

