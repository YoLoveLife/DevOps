# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 07 14:41
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
def nginx_installplaybook():
    _ext_vars = {
        'version': '1.10.1',
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/nginx',
        'file': 'nginx-{{version}}.tar.gz',
        'fro': 'http://%s/package/nginx/{{file}}' % FTP,
        'checksum': '088292d9caf6059ef328aa7dda332e44',
        'user':'nginx',
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install nginx", "nginx-server", 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="../../scripts/nginx/nginx_install.sh -v {{version}} -f {{prefix}} -u {{user}}", )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_removeplaybook():
    _ext_vars = {
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/nginx',
        'user':'nginx',
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove nginx", "nginx-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/nginx/nginx_remove.sh -f {{prefix}} -u {{user}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_controlplaybook():
    _ext_vars = {
        'control':'start',
        'pid':'/usr/local/nginx/logs/nginx.pid'
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control nginx", "nginx-server", 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/nginx/nginx_control.sh {{control}} {{pid}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_configureplaybook():
    _ext_vars = {
        'prefix':'/usr/local',
        'basedir':'{{prefix}}/nginx',
        'user':'nginx',
        'workproc':'1',
        'pid':'logs/nginx.pid',
        'workconn':'1024',
        'port':'80',
        'servername':'localhost',
        'locations':''
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("configure nginx", "nginx-server", 'no')
    task1 = PersonTask(module="template",
                   args="dest={{basedir}}/conf/nginx.conf src=../../template/nginx.j2 owner=nginx group=nginx mode=644", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

nginx_removeplaybook()
nginx_installplaybook()
nginx_controlplaybook()
