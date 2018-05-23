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
    def __init__(self, vars_dict, host_list, replay_name, key, push_mission):
        self.loader = DataLoader()
        self.options = Options(
            connection='smart', module_path='', forks=100, become=None,
            become_method=None, become_user=None, check=False,
            private_key_file=key, diff=False
        )
        self.key = key
        self.stdout_callback = callback.AnsibleCallback(replay_name, push_mission)
        self.replay_name = replay_name
        self.inventory = InventoryManager(loader=self.loader, sources=host_list.encode('utf-8')+',')

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.variable_manager.extra_vars = vars_dict
        self.play = []

    def delete_key(self):
        import os
        if os.path.exists(self.key):
            os.remove(self.key)

    def import_task(self, play_source):
        from deveops.asgi import channel_layer
        channel_layer.send(self.replay_name,{'text': 'Load Task => '})
        print('renwu',play_source)
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

            from deveops.asgi import channel_layer
            channel_layer.send(self.replay_name, {'text': 'Start => \r\n'})

            for p in self.play:
                result = tqm.run(p)
            # self.delete_key()

            channel_layer.send(self.replay_name,
                               {'text': u'执行完毕\r\n'})
            channel_layer.send(self.replay_name,
                               {'close': True})
        finally:
            if tqm is not None:
                tqm.cleanup()
