# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
from modules.persontask import PersonTask
class PersonBook():
    def __init__(self,pbname,pbhosts,pbfacts,):
        self.name=pbname
        self.hosts=pbhosts
        self.gather_facts=pbfacts
        self.tasks=[]

    def push_playbook(self):
        return dict(name=self.name,hosts=self.hosts,gather_facts=self.gather_facts,tasks=self.tasks)

    def add_task(self,task=PersonTask()):
        self.tasks.append(task.push_task())
