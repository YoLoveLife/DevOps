# -*- coding:utf-8 -*-
# !/usr/bin/python2.6
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
import django
def base_personplaybook(server='other'):
    _ext_vars={'yum_repo':'/etc/yum.repos.d',
               'md5sum':'ccd96d70ecfe3b1655c98d8dabd8dcb5',
               'url':'http://%s/repos/Zbjt.repo'%FTP,}
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("install base soft",server,'no')
    task1=PersonTask(module="shell",args="tar -cvzf ~/bk.tar.gz {{yum_repo}}/* --remove-files",)
    task2=PersonTask(module="get_url",args="checksum=md5:{{md5sum}} url={{url}} dest={{yum_repo}}/",)
    task3=PersonTask(module="shell",args="yum clean all;yum makecache;",)
    #task4=PersonTask(module="yum", args="name=gcc state=present", )
    task4=PersonTask(module="shell",args='yum install gcc -y')
    #task5=PersonTask(module="yum",args="name=make state=present",)
    task5=PersonTask(module='shell',args='yum install make -y')
    #task6=PersonTask(module="yum",args="name=libaio state=present",)
    task6=PersonTask(module='shell',args='yum install libaio -y')
    #task7=PersonTask(module="yum",args="name=libselinux-python state=present",)
    task7=PersonTask(module='shell',args='yum install libselinux-python -y')
    #task8=PersonTask(module="yum",args="name=expect state=present")
    task8=PersonTask(module='shell',args='yum install expect -y')
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    pb.add_task(task4)
    pb.add_task(task5)
    pb.add_task(task6)
    pb.add_task(task7)
    pb.add_task(task8)
    personblock.set_playbook(pb)
    personblock.run_block()