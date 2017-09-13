# -*- coding:utf-8 -*-
from inventory.maker import Maker
from yosible.tasks.tasks import Task
from yosible.run.ansiblerun import Ansible
from yosible.run.playbook import Playbook
from yosible.tasks.tasks import Tasks
class AnsibleService():
    def __init__(self,name):
        self.ansible = Ansible()
        self.maker = Maker()
        self.playbook = Playbook(pbname=name,pbfacts='no')
        self.tasks = Tasks()
        self.push_tasks()
        self.push_playbook()

    def run(self,hostlist,tasklist):
        for task in tasklist :
            t = Task(module = task.module,args=task.args)
            self.tasks.push_task(t)

        self.maker.inventory_maker(hostlist)
        self.ansible.run_playbook()
        return

    def push_tasks(self):
        self.playbook.push_tasks(self.tasks)
        return

    def push_playbook(self):
        self.ansible.set_playbook(self.playbook)

    def push_callback(self,callback):
        self.ansible.set_callback(callback)