# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
def java_installplaybook():
    _ext_vars = {
        'version':'7u79',
        'prefix':'/usr/local',
        'file':'jdk-{{version}}-linux-x64.tar.gz',
        'fro':'http://%s/package/java/{{file}}'%FTP,
        'checksum':'9222e097e624800fdd9bfb568169ccad'}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install java", "tomcat-server", 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script", args="../../scripts/java/java_install.sh -v {{version}} -f {{prefix}}", )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def java_removeplaybook():
    _ext_vars={
        'prefix':'/usr/local'
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove java", "tomcat-server", 'no')
    task1 = PersonTask(module="script", args="../../scripts/java/java_remove.sh -f {{prefix}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

java_installplaybook()