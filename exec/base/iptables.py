# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 07 16:57
# Author Yo
# Email YoLoveLife@outlook.com
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock

def iptables_configureplaybook():
    _ext_vars={'chain':"INPUT",
               'dport':'80',
               'ctstate':'NEW',
               'protocol':'tcp',
               'jump':'ACCEPT',
               }
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("configure iptables ","nginx-server",'no')
    task1=PersonTask(module="iptables",args="chain={{chain}} destination_port={{dport}} ctstate={{ctstate}} protocol={{protocol}} action=insert jump={{jump}}",)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def iptables_controlplaybook():
    _ext_vars={'control':'save'
               }
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("control iptables ","nginx-server",'no')
    task1=PersonTask(module="shell",args="/etc/init.d/iptables {{control}}",)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

iptables_configureplaybook()
iptables_controlplaybook()