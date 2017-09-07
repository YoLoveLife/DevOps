# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from collections import namedtuple
#FTP地址
FTP='192.168.254.134'
#是否启用Checksum
CHECKSUM=1

#默认的ansible host路径
HOST_LIST='/tmp/ansible.host'
#Ansible执行数值列表
OPTIONS = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
#Ansible Fork子线程个数
FORKS=100
#执行操作的连接
CONNECTION='smart'
#提权操作后成为的用户
BECOME=None
#提权操作使用的方法
BECOME_METHOD='sudo'
#提权操作后成为的用户
BECOME_USER=None



option=OPTIONS(connection='smart', module_path='', forks=FORKS, become=BECOME, become_method=BECOME_METHOD,
                          become_user=BECOME_USER, check=False)