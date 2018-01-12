# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-12
# Author Yo
# Email YoLoveLife@outlook.com
import paramiko
vm=paramiko.SSHClient()
vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
vm.connect('114.55.126.93',username='root',key_filename='/home/yo/.ssh/id_rsa',port=52000)
vmtransport = vm.get_transport()
dest_addr = ('10.101.30.188',22)
local_addr = ('114.55.126.93',52000)
vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
jhost = paramiko.SSHClient()
jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
jhost.connect('10.101.30.188', username='root',key_filename='/home/yo/.ssh/id_rsa',sock=vmchannel)

stdin,stdout,stderr = jhost.exec_command('hostname')
print(stdout.read())
jhost.close()
vm.close()