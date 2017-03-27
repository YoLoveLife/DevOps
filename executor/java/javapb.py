# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
from scripts import SCRIPTS_DIR
from template import TEMPLATEDIR
def java_installplaybook(server='other',version='7u79',prefix='/usr/local',checksum='9222e097e624800fdd9bfb568169ccad'):
    _ext_vars = {
        'version':version,
        'prefix':prefix,
        'file':'jdk-{{version}}-linux-x64.tar.gz',
        'fro':'http://%s/package/java/{{file}}'%FTP,
        'checksum':checksum}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install java", server, 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script", args="%s/java/java_install.sh -v {{version}} -f {{prefix}}"%SCRIPTS_DIR, )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def java_removeplaybook(server='other',prefix='/usr/local'):
    _ext_vars={
        'prefix':prefix
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove java",server, 'no')
    task1 = PersonTask(module="script", args="%s/java/java_remove.sh -f {{prefix}}"%SCRIPTS_DIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

if __name__=='__main__':
    java_installplaybook(server='tomcat-server')
    java_removeplaybook(server='tomcat-server')