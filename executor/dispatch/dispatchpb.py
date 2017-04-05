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
def dispatch_getcnf(cnffile):
    t=time.time()
    _ext_vars={'cnffile':cnffile,
               'filename':t,
               }
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("dispatch getcnf",'no')
    task1=PersonTask(module="fetch",args="src={{cnffile}} dest=/tmp/{{filename}} flat=yes",)
    #task2=PersonTask(module="shell",args="find ./ -name 'hosts.*.[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\@[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\~' -mmin +60 -exec rm -f {} \;")
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()
    f = open(FILENAME%t)
    try:
        str=f.read()
    finally:
        f.close()
        os.remove(FILENAME%t)
    return str

print(dispatch_getcnf('/etc/hosts'))