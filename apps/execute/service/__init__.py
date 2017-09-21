# -*- coding:utf-8 -*-
from yosible.tasks.tasks import Task
from yosible.run.ansiblerun import Ansible
from yosible.run.playbook import Playbook
from yosible.tasks.tasks import Tasks
from operation.models import Script
__metaclass__ = type
class AnsibleService():
    def __init__(self,filename):
        self.ansible = Ansible(filename)
        self.playbook = Playbook(pbname='null',pbfacts='no')
        self.tasks = Tasks()
        self.push_tasks()
        self.push_playbook()

    def run(self,tasklist,maker):
        for task in tasklist :
            t = Task(module = task.module,args=task.args)
            #如果为脚本 则单独将脚本文件写出来
            if task.module == u'script':
                script = Script.objects.get(id=int(str(task.args)))
                t.args = maker.script_maker(script_id=str(script.id),script=script.formatScript())
            self.tasks.push_task(t)
        result = self.ansible.run_playbook()
        maker.inventory_clear()

        return result

    def push_makername(self):
        return self.maker.filename

    def push_tasks(self):
        self.playbook.push_tasks(self.tasks)
        return

    def push_playbook(self):
        self.ansible.set_playbook(self.playbook)

    def push_callback(self,callback):
        self.ansible.set_callback(callback)