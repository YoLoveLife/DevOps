# -*- coding:utf-8 -*-
# !/usr/bin/python
# Time 07 14:41
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
from scripts import SCRIPTS_DIR
from template import TEMPLATEDIR
def nginx_installplaybook(version='1.10.1',prefix='/usr/local',checksum='088292d9caf6059ef328aa7dda332e44'):
    _ext_vars = {
        'version': version,
        'prefix': prefix,
        'basedir': '{{prefix}}/nginx',
        'file': 'nginx-{{version}}.tar.gz',
        'fro': 'http://%s/package/nginx/{{file}}' % FTP,
        'checksum': checksum,
        'user':'nginx',
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install nginx", 'no')
    #task0=PersonTask(module='yum',args='name=pcre-devel state=present')
    task0=PersonTask(module='shell',args='yum install pcre-devel -y')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="%s/nginx/nginx_install.sh -v {{version}} -f {{prefix}} -u {{user}}"%SCRIPTS_DIR, )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task0)
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_removeplaybook(prefix='/usr/local',):
    _ext_vars = {
        'prefix': prefix,
        'basedir': '{{prefix}}/nginx',
        'user':'nginx',
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove nginx", 'no')
    task1 = PersonTask(module="script",
                       args="%s/nginx/nginx_remove.sh -f {{prefix}} -u {{user}}"%SCRIPTS_DIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_controlplaybook(control='start',pid='/usr/local/nginx/logs/nginx.pid'):
    _ext_vars = {
        'control':control,
        'pid':pid
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control nginx", 'no')
    task1 = PersonTask(module="script",
                       args="%s/nginx/nginx_control.sh {{control}} {{pid}}"%SCRIPTS_DIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_configureplaybook(prefix='/usr/local',workproc='1',pid='logs/nginx.pid',workconn='1024',port='80',servername='localhost',locations=''):
    _ext_vars = {
        'prefix':prefix,
        'basedir':'{{prefix}}/nginx',
        'user':'nginx',
        'workproc':workproc,
        'pid':pid,
        'workconn':workconn,
        'port':port,
        'servername':servername,
        'locations':locations,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("configure nginx", 'no')
    task1 = PersonTask(module="template",
                   args="dest={{basedir}}/conf/nginx.conf src=%s/nginx.j2 owner=nginx group=nginx mode=644"%TEMPLATEDIR, )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

