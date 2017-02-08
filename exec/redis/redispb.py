# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
def redis_installplaybook():
    _ext_vars = {
        'version':'3.2.4',
        'prefix':'/usr/local',
        'basedir':'{{prefix}}/redis',
        'user':'redis',
        'file':'redis-{{version}}.tar.gz',
        'fro':'http://%s/package/redis/{{file}}'%FTP,
        'checksum':'2f8b49e8004fbbfc807ca7f5faeabec8'}
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install redis", "redis-server", 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script", args="../../scripts/redis/redis_install.sh -v {{version}} -f {{prefix}} -u {{user}}", )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def redis_removeplaybook():
    _ext_vars={
        'prefix':'/usr/local',
        'user': 'redis'
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install redis", "redis-server", 'no')
    task1 = PersonTask(module="script", args="../../scripts/redis/redis_remove.sh -u {{user}} -f {{prefix}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def redis_controlplaybook():
    _ext_vars={
        'control':'stop'
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control redis", "redis-server", 'no')
    task1 = PersonTask(module="script", args="../../scripts/redis/redis_control.sh {{control}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()


def redis_configureplaybook():
    _ext_vars={
        'prefix':   '/usr/local',
        'basedir':  '{{prefix}}/redis',
        'bind':'0.0.0.0',
        'port':'6379',
        'appendonly':"yes",
        'noonrewrite':'no',
        'logfile':'{{basedir}}/{{port}}.log',
        'saveoptions':'save 900 300\nsave 30 10\nsave 2000 1',
        'dbfilename':'{{port}}.rdb',
        'dir':'{{basedir}}/data',
        #'slaveof':'slaveof mip mport',
        'slaveof':'',
        #'masterauth':'masterauth Redis',
        'masterauth':'',
        #'cluster_enabled':'cluster-enabled yes',
        'cluster_enabled':'',
        #'cluster_config_file':'cluster-config-file nodes-{{port}}.conf',
        'cluster_config_file':'',
        'extend':''
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control redis", "redis-server", 'no')
    task1 = PersonTask(module="template", args="dest=/etc/redis.conf src=../../template/redis.j2 owner=redis group=redis mode=644", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()
