# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock

def mysql_installplaybook():
    _ext_vars = {
        'version': '10.1.12',
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/mysql',
        'datadir':'{{basedir}}/data',
        'user': 'mysql',
        #'file': 'mariadb-{{version}}-linux-{{ansible_architecture}}.tar.gz',
        'file': 'mariadb-{{version}}-linux-x86_64.tar.gz',
        'fro': 'http://%s/package/mysql/{{file}}' % FTP,
        'checksum': '30a86202c8fe30ad3548988a7ddbf5a3'}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install mysql", "mysql-server", 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="../../scripts/mysql/mysql_install.sh -v {{version}} -f {{prefix}} -u {{user}} -d {{datadir}}", )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_removeplaybook():
    _ext_vars = {
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/mysql',
        'datadir':'{{basedir}}/data',
        'user': 'mysql',
        'conf':'/etc/my.cnf',}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove mysql", "mysql-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/mysql/mysql_remove.sh -f {{prefix}} -u {{user}} -d {{datadir}} -c {{conf}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_controlplaybook():
    _ext_vars={
        'control':'start',
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control mysql", "mysql-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/mysql/mysql_control.sh {{control}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_initializationplaybook():
    _ext_vars={
        'mysqlpasswd':'000000',
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("initialization mysql", "mysql-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/mysql/mysql_answer.exp {{mysqlpasswd}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def mysql_configureplaybook():
    _ext_vars={
        'port':'3306',
        'socket':'/tmp/mysql.sock',
        'basedir':'/usr/local/mysql',
        'datadir':'/usr/local/mysql/data',
        'key_buffer_size':'256M',
        'table_open_cache':'256',
        'sort_buffer_size':'1M',
        'read_buffer_size':'1M',
        'read_rnd_buffer_size':'4M',
        'query_cache_size':'16M',
        'thread_cache_size':'8',
        'server_id':'1',
        'extend':'',
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("configure mysql", "mysql-server", 'no')
    task1 = PersonTask(module="template", args="dest=/etc/my.cnf src=../../template/my.j2 owner=mysql group=mysql mode=644", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

mysql_removeplaybook()
