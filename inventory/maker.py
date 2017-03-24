# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 06 14:50
# Author Yo
# Email YoLoveLife@outlook.com
import os
FILE=r"/tmp/ansible.host"
def inventory_maker(host_list):
    if os.path.exists(FILE):
        os.remove(FILE)
    output=open(FILE,'w')
    for host in host_list:
        output.writelines(host+"\n")
    output.close()

def inventory_clear():
    if os.path.exists(FILE):
        os.remove(FILE)