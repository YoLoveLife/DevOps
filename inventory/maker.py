# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 06 14:50
# Author Yo
# Email YoLoveLife@outlook.com
import os
import time
FILENAME = r"/tmp/%s%s"
SSHPORT = "ansible_ssh_port="
SSHUSER = "ansible_ssh_user="
SUDOPASS = "ansible_sudo_pass="
class Maker():
    def __init__(self):
        self.timestamp = str(time.time())
        self.filename=FILENAME%(self.timestamp,'')

    def set_filename(self,filename):
        self.filename=FILENAME%(filename,'')

    def inventory_maker(self,hosts):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        output=open(self.filename,'w')
        for host in hosts:
            str = host.service_ip + \
            " " + SSHPORT + host.sshport + \
            " " + SSHUSER + host.normal_user + \
            " " + SUDOPASS + host.sshpasswd + '\n'
            output.writelines(str)
        output.close()
        return self.filename

    def inventory_clear(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        return self.filename

    def script_maker(self,script_id,script):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        script_name = FILENAME%(self.timestamp,'-'+script_id)
        output = open(script_name,'w')
        output.writelines(script)
        output.close()
        return script_name


