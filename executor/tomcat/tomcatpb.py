# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
from scripts import SCRIPTS_DIR

def tomcat_installplaybook(server='other',version='7.0.72',prefix='/usr/local',java_opts='',checksum='c24bfae15bb9c510451a05582aae634d'):
    _ext_vars = {
        'version':version,
        'prefix': prefix,
        'basedir': '{{prefix}}/tomcat',
        'java_home':'{{prefix}}/java',
        'java_opts':java_opts,
        'file': 'apache-tomcat-{{version}}.tar.gz',
        'fro': 'http://%s/package/tomcat/{{file}}' % FTP,
        'checksum': checksum}
    personblock = PersonBlock()
    print(SCRIPTS_DIR)
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install tomcat", server, 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="%s/tomcat/tomcat_install.sh -v {{version}} -f {{prefix}}"%SCRIPTS_DIR, )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    task4 = PersonTask(module="template",
                       args="dest={{basedir}}/bin/setenv.sh src=../template/setenv.j2 owner=root group=root mode=755", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    pb.add_task(task4)
    personblock.set_playbook(pb)
    personblock.run_block()

def tomcat_removeplaybook(server='other',prefix='/usr/local'):
    _ext_vars = {
        'prefix': prefix,
        'basedir': '{{prefix}}/tomcat',
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove tomcat", server, 'no')
    task1 = PersonTask(module="script",
                       args="%s/tomcat/tomcat_remove.sh -f {{prefix}}"%SCRIPTS_DIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def tomcat_controlplaybook(server='other',control='start'):
    _ext_vars = {
        'control':control,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control tomcat",server, 'no')
    task1 = PersonTask(module="script",
                       args="%s/tomcat/tomcat_control.sh {{control}}"%SCRIPTS_DIR,)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

if __name__=='__main__':
    tomcat_removeplaybook(server='tomcat-server')
    tomcat_installplaybook(server='tomcat-server')
    tomcat_controlplaybook(server='tomcat-server')