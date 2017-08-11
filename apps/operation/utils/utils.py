# -*- coding:utf-8 -*-
import constant
def bash_writer(*args,**kwargs):
    return bash_head(*args,**kwargs)

def bash_head(author,time,*args,**kwargs):#author time
    str="#!/bin/bash"+"\n"
    str+="#Author "+author + "\n"
    str+="#Time " + time + "\n"
    return str+args_maker(*args,**kwargs)

def args_maker(*args,**kwargs):
    str=""
    OPTIONS=""
    CASE_ITEMS=""
    for key in kwargs:
        if kwargs[key]=="1":
            OPTIONS+=key+':'
            CASE_ITEMS+=constant.EXTEND_CASE_ITEM%(key,key)
        else:
            OPTIONS+=key
            CASE_ITEMS+=constant.SIMPLE_CASE_ITEM%(key,key)
        OPTIONS+=','
    command = 'ARGS=`getopt --long %s -- "$@"`'%(OPTIONS)
    str+=constant.FUNCTION_ARGS%(command,CASE_ITEMS+constant.CASE_END)
    str+='Args $@\n'
    return str

if __name__ == "__main__":
    kwargs={'prefix':'1','version':'2','good':'1'}
    print(bash_writer(author='Yo',time='2017-8-11 16:44:13',**kwargs))