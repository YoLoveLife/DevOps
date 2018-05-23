# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-6
# Author Yo
# Email YoLoveLife@outlook.com
from ansible.inventory import Host,Group,Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from deveops.utils.aes import decrypt
__all__ = ['YoInventory','YoHost']
class YoHost(Host):
    def __init__(self,host):
        self.host = host
        self.name = host.connect_ip
        self.port = host.sshport
        super(YoHost,self).__init__(self.name,self.port)
        self.set_all_variable()

    def set_all_variable(self):
        self.set_variable('ansible_host', self.name)
        self.set_variable('ansible_port', self.port)
        self.set_variable('ansible_user', self.host.sys_user.username)
        # self.set_variable('ansible_ssh_pass', self.host.sshpasswd) #密码登陆
        self.set_variable("ansible_become", True)
        self.set_variable("ansible_become_method", 'sudo')
        self.set_variable("ansible_become_user", 'root')
        self.set_variable("ansible_become_pass", decrypt(self.host.sshpasswd))

class YoInventory(Inventory):
    def __init__(self,host_list):
        if host_list is None:
            host_list = []
        else:
            self.host_list = host_list
            self.loader = DataLoader()
            self.variable_manager = VariableManager()
            super(YoInventory,self).__init__(self.loader,self.variable_manager,self.host_list)

    def parse_inventory(self,host_list):
        all = Group('all')
        for host in host_list:
            h = YoHost(host)
            all.add_host(h)
        self.groups = dict(all=all)


