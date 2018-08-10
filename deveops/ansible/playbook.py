# -*- coding:utf-8 -*-
from __future__ import absolute_import,unicode_literals
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
__all__ = [
    "Playbook"
]

from collections import namedtuple

Options = namedtuple('Options', ['connection', 'module_path', 'forks',
                                 'become', 'become_method', 'become_user', 'check', 'private_key_file','diff'])


class Playbook(object):
    def __init__(self, host_list, key, callback):
        self.loader = DataLoader()
        self.options = Options(
            connection='smart', module_path='', forks=100, become=None,
            become_method=None, become_user=None, check=False,
            private_key_file=key, diff=False
        )
        self.key = key
        self.stdout_callback = callback
        self.inventory = InventoryManager(loader=self.loader, sources=host_list)#+',')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.play = []


    def delete_key(self):
        import os
        if os.path.exists(self.key):
            os.remove(self.key)


    def import_vars(self, vars_dict):
        vars_dict['KEY'] = self.key
        self.variable_manager.extra_vars = vars_dict


    def import_task(self, play_source):
        for source in play_source:
            self.play.append(
                Play().load(
                    source,
                    variable_manager=self.variable_manager,
                    loader=self.loader
                )
            )

    def run(self):
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory = self.inventory,
                variable_manager = self.variable_manager,
                loader = self.loader,
                options = self.options,
                passwords = {},
                stdout_callback = self.stdout_callback
            )
            for p in self.play:
                result = tqm.run(p)
            # self.delete_key()
        finally:
            if tqm is not None:
                tqm.cleanup()
