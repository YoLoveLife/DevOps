# -*- coding:utf-8 -*-
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ops.ansible import callback

__all__ = [
    "Options", "Playbook"
]

Options = namedtuple('Options', ['connection', 'module_path', 'forks',
                                 'become', 'become_method', 'become_user', 'check', 'private_key_file','diff'])


class Playbook(object):
    def __init__(self, vars_dict, host_list, consumer, key, push_mission):
        self.loader = DataLoader()
        self.options = Options(
            connection='smart', module_path='', forks=100, become=None,
            become_method=None, become_user=None, check=False,
            private_key_file=key, diff=False
        )
        self.key = key
        self.stdout_callback = callback.AnsibleCallback(consumer, push_mission)
        self.consumer = consumer
        print('ddr',host_list)
        self.inventory = InventoryManager(loader=self.loader, sources=host_list+',')

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.variable_manager.extra_vars = vars_dict
        self.play = []

    def delete_key(self):
        import os
        if os.path.exists(self.key):
            os.remove(self.key)

    def import_task(self, play_source):
        self.consumer.send('Load Task =>\r\n')
        for source in play_source:
            self.play.append(Play().load(source, variable_manager=self.variable_manager, loader=self.loader))

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
            self.consumer.send("Start => \r\n")
            for p in self.play:
                result = tqm.run(p)
            # self.delete_key()

            self.consumer.send('执行完毕\r\n')
        finally:
            self.consumer.close()
            if tqm is not None:
                tqm.cleanup()
