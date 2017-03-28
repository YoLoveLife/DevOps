# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:52
# Author Yo
# Email YoLoveLife@outlook.com
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock

def shell_book(shell='hostname'):
    _ext_vars={'shell':shell,
               }
    personblock=PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb=PersonBook("shell iptables ",'no')
    task1=PersonTask(module="shell",args="{{shell}}",)
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()