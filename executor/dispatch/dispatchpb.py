# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 01 08:36
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
import time,os
from executor.dispatch import REDIS_CONF,MYSQL_CONF,NGINX_CONF,TOMCAT_CONF
FILENAME=r'/tmp/%s'
BACK_NAME='\'%s.*.[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\@[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\~\''
def dispatch_getcnf(cnffile):
    t=time.time()
    _ext_vars={'cnffile':cnffile,
               'filename':t,
               }
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("dispatch getcnf",'no')
    task1=PersonTask(module="fetch",args="src={{cnffile}} dest=/tmp/{{filename}} flat=yes",)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()
    f = open(FILENAME%t)
    try:
        str=f.read()
    finally:
        f.close()
        #os.remove(FILENAME%t)
    return (str,FILENAME%t)

def dispatch_cnf2file(str,file):#将字符串转换成配置文件
    f=open(file,'w+')
    try:
        f.write(str)
    finally:
        f.close()
    return file

def dispatch_setcnf(src,dest):#src=/tmp/aaaa dest=/etc/hosts dir=/etc file=hosts dispatch_srcdeploy解析地址
    data=dispatch_srcdeploy(dest)
    dir=data[0]
    file=data[1]
    _ext_vars = {
                'src':src,
                'dest':dest,
                'dir': dir,
                'file': file,
                 }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("dispatch setcnf", 'no')
    task1 = PersonTask(module="copy", args="src={{src}} dest={{dest}} backup=yes", )
    task2 = PersonTask(module="shell",args="find %s -name %s -mmin +61 -exec rm -f {} \;"%(dir,BACK_NAME%file))#删除旧分配备份
    pb.add_task(task1)
    pb.add_task(task2)
    personblock.set_playbook(pb)
    personblock.run_block()

def dispatch_srcdeploy(src):
    list=src.split('/')
    dir="/"
    for i in range(len(list)-1):
        dir+=list[i]
    return (dir,list[len(list)-1])