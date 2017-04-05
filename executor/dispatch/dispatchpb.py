# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 01 08:36
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
from executor.dispatch import REDIS_CONF,MYSQL_CONF,NGINX_CONF,TOMCAT_CONF

def dispatch_getcnf(taskname,cnffile):
    _ext_vars={'filename':taskname,
               'cnffile':cnffile,
               }
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("dispatch getcnf",'no')
    task1=PersonTask(module="fetch",args="src={{cnffile}} dest=/tmp/{{filename}} flat=yes",)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

dispatch_getcnf('redis-server','/etc/hosts')
f=open(r'/tmp/redis-server')
print(f.read())
f.close()