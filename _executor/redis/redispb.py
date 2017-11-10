# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from utils import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
from scripts import SCRIPTS_DIR
from template import TEMPLATEDIR
def redis_installplaybook(version='3.2.4',prefix='/usr/local',checksum='2f8b49e8004fbbfc807ca7f5faeabec8',datadir='{{prefix}}/redis/data'):
    _ext_vars = {
        'version':version,
        'prefix':prefix,
        'basedir':'{{prefix}}/redis',
        'user':'redis',
        'datadir':datadir,
        'file':'redis-{{version}}.tar.gz',
        'fro':'http://%s/package/redis/{{file}}'%FTP,
        'checksum':checksum
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install redis",'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script", args="%s/redis/redis_install.sh -v {{version}} -f {{prefix}} -u {{user}}"%SCRIPTS_DIR, )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    task4 = PersonTask(module="file",args="dest={{datadir}} mode=755 owner=root state=directory")
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    pb.add_task(task4)
    personblock.set_playbook(pb)
    personblock.run_block()

def redis_removeplaybook(prefix='/usr/local'):
    _ext_vars={
        'prefix':prefix,
        'user': 'redis'
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install redis", 'no')
    task1 = PersonTask(module="script", args="%s/redis/redis_remove.sh -u {{user}} -f {{prefix}}"%SCRIPTS_DIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def redis_controlplaybook(control='start',passwd='000000'):
    _ext_vars={
        'control':control,
        'passwd':passwd,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control redis", 'no')
    if control=='stop':
        task1 = PersonTask(module="script", args="%s/redis/redis_control.sh {{control}} {{passwd}}"%SCRIPTS_DIR, )
    else:
        task1 = PersonTask(module="script", args="%s/redis/redis_control.sh {{control}}"%SCRIPTS_DIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()


def redis_configureplaybook(version='3.2.4',prefix='/usr/local',bind='0.0.0.0',port='6379',appendonly='yes',noonrewrite='no',saveoptions='save 900 300\nsave 30 10\nsave 2000 1',datadir='{{basedir}}',requirepass='000000',slaveof='',masterauth='',cluster_enabled='',cluster_config_file='',extend=''):
    _ext_vars={
        'prefix':   prefix,
        'basedir':  '{{prefix}}/redis',
        'bind':bind,
        'port':port,
        'appendonly':appendonly,
        'noonrewrite':noonrewrite,
        'logfile':'{{basedir}}/{{port}}.log',
        'saveoptions':saveoptions,
        'dbfilename':'{{port}}.rdb',
        'dir':datadir,
        'requirepass':requirepass,
        #'slaveof':'slaveof mip mport',
        'slaveof':slaveof,
        #'masterauth':'masterauth Redis',
        'masterauth':masterauth,
        #'cluster_enabled':'cluster-enabled yes',
        'cluster_enabled':cluster_enabled,
        #'cluster_config_file':'cluster-config-file nodes-{{port}}.conf',
        'cluster_config_file':cluster_config_file,
        'extend':extend,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control redis", 'no')
    task1 = PersonTask(module="template", args="dest=/etc/redis.conf src=%s/redis/redis%s.j2 owner=redis group=redis mode=644"%(TEMPLATEDIR,version), )
    print('0000000')
    print("dest=/etc/redis.conf src=%s/redis/redis%s.j2 owner=redis group=redis mode=644"%(TEMPLATEDIR,version))
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()