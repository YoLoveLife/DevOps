# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 26 02:04
# Author Yo
# Email YoLoveLife@outlook.com
import os
import psutil
import re
import string
JSTACK="/usr/local/java/bin/jstack"
DUI="jstack -gcutil 1000 10"
def getJVMInfo():
    process_list=psutil.process_iter()
    for p in process_list:
        if p.name() == "java":
            JVMPID=p.pid
            THREADS=p.num_threads()
            return (JVMPID,THREADS)

def getThread(JVMPID):
    COMMMD=JSTACK+" -l "+str(JVMPID)
    print(COMMMD)
    out=os.popen(COMMMD)
    return out.read()

def analysisThead(string):
    r1=re.compile(r'\".*\"')
    r2=re.compile(r'java.lang.Thread.State:\w+.*\w+')
    m=r2.match(string)
    thread_state=r2.findall(string)
    thread_list=r1.findall(string)
    theadinfo=r1.split(string)
    return thread_list

#print(getJVMInfo())
str=getThread(getJVMInfo()[0])
print(analysisThead(str))

'''
NEW 线程被NEW出来 未调用start方法
RUNNABLE 线程已经调用了start方法 但是run方法可能运行也可能没有运行
BLOCKED 线程进入了synchronized同步块
WAITING 调用了对象的wait方法
TIMED_WAITING
TERMINATED run方法退出
'''
