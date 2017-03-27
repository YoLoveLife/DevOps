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
def mysql_installplaybook(server='other',version='10.1.12',prefix='/usr/local',checksum='30a86202c8fe30ad3548988a7ddbf5a3'):
    _ext_vars = {
        'version': version,
        'prefix': prefix,
        'basedir': '{{prefix}}/mysql',
        'datadir':'{{basedir}}/data',
        'user': 'mysql',
        #'file': 'mariadb-{{version}}-linux-{{ansible_architecture}}.tar.gz',
        'file': 'mariadb-{{version}}-linux-x86_64.tar.gz',
        'fro': 'http://%s/package/mysql/{{file}}' % FTP,
        'checksum':checksum}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install mysql",server, 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="%s/mysql/mysql_install.sh -v {{version}} -f {{prefix}} -u {{user}} -d {{datadir}}"%SCRIPTS_DIR, )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_removeplaybook(server='other',prefix='/usr/local'):
    _ext_vars = {
        'prefix': prefix,
        'basedir': '{{prefix}}/mysql',
        'datadir':'{{basedir}}/data',
        'user': 'mysql',
        'conf':'/etc/my.cnf',}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove mysql", server, 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/mysql/mysql_remove.sh -f {{prefix}} -u {{user}} -d {{datadir}} -c {{conf}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_controlplaybook(server='other',control='start'):
    _ext_vars={
        'control':control,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control mysql", server, 'no')
    task1 = PersonTask(module="script",
                       args="%s/mysql/mysql_control.sh {{control}}"%TEMPLATEDIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_initializationplaybook(server='other',mysqlpasswd='000000'):
    _ext_vars={
        'mysqlpasswd':mysqlpasswd,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("initialization mysql", server, 'no')
    task1 = PersonTask(module="script",
                       args="%s/mysql/mysql_answer.exp {{mysqlpasswd}}"%TEMPLATEDIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_configureplaybook(server='other',port='3306',socket='/tmp/mysql.sock',prefix='/usr/local',datadir='/usr/local/mysql/data',
                                    key_buffer_size='256M',table_open_cache='256',sort_buffer_size='1M',read_buffer_size='1M',read_rnd_buffer_size='4M',
                            query_cache_size='16M',thread_cache_size='8',server_id='1',extend=''):
    _ext_vars={
        'port':port,
        'socket':socket,
        'prefix':prefix,
        'basedir':'{{prefix}}/mysql',
        'datadir':datadir,
        'key_buffer_size':key_buffer_size,
        'table_open_cache':table_open_cache,
        'sort_buffer_size':sort_buffer_size,
        'read_buffer_size':read_buffer_size,
        'read_rnd_buffer_size':read_rnd_buffer_size,
        'query_cache_size':query_cache_size,
        'thread_cache_size':thread_cache_size,
        'server_id':server_id,
        'extend':extend,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("configure mysql", server, 'no')
    task1 = PersonTask(module="template", args="dest=/etc/my.cnf src=%s/my.j2 owner=mysql group=mysql mode=644"%TEMPLATEDIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

