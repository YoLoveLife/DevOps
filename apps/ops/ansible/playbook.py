# -*- coding:utf-8 -*-
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import callback

__all__ = [
    "Options", "Playbook"
]

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'private_key_file'])


class Playbook(object):
    def __init__(self, host_list, replay_name, key):
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        f = open('/tmp/ddr.pri', 'w')
        f.write(key)
        f.close()
        self.options = Options(connection='smart', module_path='', forks=100, become=None,
                               become_method=None, become_user=None, check=False, private_key_file='/tmp/ddr.pri')
        self.stdout_callback = callback.AnsibleCallback(replay_name)
        self.replay_name = replay_name
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=host_list)
        self.variable_manager.set_inventory(self.inventory)
        self.play = None

    def import_task(self, play_source):
        from deveops.asgi import channel_layer
        channel_layer.send(self.replay_name,{'text': 'Load Task => '})

        self.play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

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

            result = tqm.run(self.play)

            from deveops.asgi import channel_layer
            channel_layer.send(self.replay_name,
                               {'text': 'Done\r\n'})
            channel_layer.send(self.replay_name,
                               {'close': True})
        finally:
            if tqm is not None:
                tqm.cleanup()
