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
    thread_list=r1.findall(string)
    theadinfo=r1.split(string)


print(getThread(getJVMInfo()[0]))
