# -*- coding:utf-8 -*-
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.errors import AnsibleParserError,AnsibleUndefinedVariable
from django.conf import settings
from ops.ansible import callback

__all__ = [
    "Options", "Playbook"
]

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'host_key_checking',
                                 'become', 'become_method', 'become_user', 'check', 'private_key_file','diff'])


class Playbook(object):
    def __init__(self, host_list, consumer, key, push_mission):
        self.loader = DataLoader()
        self.options = Options(
            connection='smart', module_path='', forks=100, become=None,
            become_method=None, become_user=None, check=False,
            private_key_file=key, diff=False
        )
        self.key = key
        self.stdout_callback = callback.AnsibleCallback(consumer, push_mission)
        self.consumer = consumer
        self.push_mission = push_mission
        self.inventory = InventoryManager(loader=self.loader, sources=host_list+',')

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.play = []

    def delete_key(self):
        import os
        if os.path.exists(self.key):
            os.remove(self.key)

    def import_vars(self, vars_dict):
        self.push_mission.status = settings.OPS_PUSH_MISSION_IMPORT_VAR
        try:
            vars_dict['KEY']=self.key
            self.variable_manager.extra_vars = vars_dict
            self.push_mission.results_append('参数载入成功;')
            self.push_mission.results_append(vars_dict)
        except AnsibleUndefinedVariable as e:
            self.push_mission.results_append('参数识别失败;')
            self.consumer.send('ERROR')
            self.consumer.close()
        self.consumer.send('OK')

    def import_task(self, play_source):
        self.push_mission.status = settings.OPS_PUSH_MISSION_IMPORT_TASKS
        try:
            self.push_mission.results_append(play_source)
            for source in play_source:
                self.play.append(Play().load(source, variable_manager=self.variable_manager, loader=self.loader))
            self.push_mission.results_append('任务载入成功;')
        except AnsibleParserError as e:
            self.push_mission.results_append('错误或者丢失模块;')
            self.consumer.send('ERROR')
            self.consumer.close()
        self.consumer.send('OK')

    def run(self):
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords={},
                stdout_callback=self.stdout_callback
            )
            for p in self.play:
                result = tqm.run(p)
            self.delete_key()
            self.push_mission.status = settings.OPS_PUSH_MISSION_SUCCESS
            self.consumer.send("SUCCESS")
        finally:
            self.consumer.close()
            if tqm is not None:
                tqm.cleanup()
