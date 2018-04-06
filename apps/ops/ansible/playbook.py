# -*- coding:utf-8 -*-
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import callback

__all__ = [
    "Options", "Playbook"
]

Options = namedtuple('Options', ['connection', 'module_path', 'forks',
                                 'become', 'become_method', 'become_user', 'check', 'private_key_file','diff'])


class Playbook(object):
    def __init__(self, host_list, replay_name, key):
        self.loader = DataLoader()
        self.options = Options(
            connection='smart', module_path='', forks=100, become=None,
            become_method=None, become_user=None, check=False,
            private_key_file=self.write_key(key), diff=False
        )
        self.stdout_callback = callback.AnsibleCallback(replay_name)
        self.replay_name = replay_name
        print(host_list)
        print('host_list',host_list.encode('utf-8'))
        self.inventory = InventoryManager(loader=self.loader, sources=host_list.encode('utf-8')+',')

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.play = None

    def write_key(self,key):
        try:
            f = open('/tmp/ddr.pri', 'w')
            f.write(key)
            f.close()
        except Exception:
            return '~/.ssh/id_rsa'
        return '/tmp/ddr.pri'

    def import_task(self, play_source):
        from deveops.asgi import channel_layer
        channel_layer.send(self.replay_name,{'text': 'Load Task => '})

        self.play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

    def extra_vars(self,vars):
        self.variable_manager.extra_vars(vars)

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
