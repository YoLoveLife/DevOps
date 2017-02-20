# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
def tomcat_installplaybook():
    _ext_vars = {
        'version': '7.0.72',
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/tomcat',
        'java_home':'{{prefix}}/java',
        'java_opts':'',
        'file': 'apache-tomcat-{{version}}.tar.gz',
        'fro': 'http://%s/package/tomcat/{{file}}' % FTP,
        'checksum': 'c24bfae15bb9c510451a05582aae634d'}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install tomcat", "tomcat-server", 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="../../scripts/tomcat/tomcat_install.sh -v {{version}} -f {{prefix}}", )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    task4 = PersonTask(module="template",
                       args="dest={{basedir}}/bin/setenv.sh src=../../template/setenv.j2 owner=root group=root mode=755", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    pb.add_task(task4)
    personblock.set_playbook(pb)
    personblock.run_block()

def tomcat_removeplaybook():
    _ext_vars = {
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/tomcat',
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove tomcat", "tomcat-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/tomcat/tomcat_remove.sh -f {{prefix}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def tomcat_controlplaybook():
    _ext_vars = {
        'control': 'stop',
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control tomcat", "tomcat-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/tomcat/tomcat_control.sh {{control}}",)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

tomcat_controlplaybook()