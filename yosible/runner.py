# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-7
# Author Yo
# Email YoLoveLife@outlook.com
from collections import namedtuple
import ansible.constants as C
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.vars import load_extra_vars
from ansible.utils.vars import load_options_vars
from yosible.inventory import YoHost,YoInventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

class AdHocRunner(object):
    Options = namedtuple("Options", [
        'connection', 'module_path', 'private_key_file', "remote_user",
        'timeout', 'forks', 'become', 'become_method', 'become_user',
        'check', 'extra_vars',
        ]
    )

    def __init__(self,
                 hosts=C.DEFAULT_HOST_LIST,
                 forks=C.DEFAULT_FORKS,  # 5
                 timeout=C.DEFAULT_TIMEOUT,  # SSH timeout = 10s
                 remote_user=C.DEFAULT_REMOTE_USER,  # root
                 module_path=None,  # dirs of custome modules
                 connection_type="smart",
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=False,
                 passwords=None,
                 extra_vars=None,
                 private_key_file=None,
                 gather_facts='no'):
        self.pattern = ''
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.gather_facts = gather_facts
        self.options = self.Options(
            connection=connection_type,
            timeout=timeout,
            module_path=module_path,
            forks=forks,
            become=become,
            become_method=become_method,
            become_user=become_user,
            check=check,
            remote_user=remote_user,
            extra_vars=extra_vars or [],
            private_key_file=private_key_file,
        )
        self.variable_manager.extra_vars = load_extra_vars(self.loader,
                                                           options=self.options)
        self.variable_manager.options_vars = load_options_vars(self.options)
        self.passwords = passwords or {}
        self.inventory = YoInventory(hosts)
        self.variable_manager.set_inventory(self.inventory)
        self.tasks = []
        self.play_source = None
        self.play = None
        self.runner = None

    def set_callback(self,callback):
        self.results_callback=callback

    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '%s' module." % module_name
            print(err)
            return False
        return True

    def run(self, task_tuple, pattern='all', task_name='Ansible Ad-hoc'):
        """
        :param task_tuple:  (('shell', 'ls'), ('ping', ''))
        :param pattern:
        :param task_name:
        :return:
        """
        for task in task_tuple:
            if not self.check_module_args(task.module,task.args):
                return
            self.tasks.append(
                dict(action=dict(
                    module=task.module,
                    args=task.args,
                ))
            )

        self.play_source = dict(
            name=task_name,
            hosts=pattern,
            gather_facts=self.gather_facts,
            tasks=self.tasks
        )

        self.play = Play().load(
            self.play_source,
            variable_manager=self.variable_manager,
            loader=self.loader,
        )

        self.runner = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            stdout_callback=self.results_callback,
        )

        # if not self.inventory.list_hosts("all"):
        #     raise AnsibleError("Inventory is empty.")
        #
        # if not self.inventory.list_hosts(self.pattern):
        #     raise AnsibleError(
        #         "pattern: %s  dose not match any hosts." % self.pattern)

        try:
            self.runner.run(self.play)
        finally:
            if self.runner:
                self.runner.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()

    def clean_result(self):
        """
        :return: {
            "success": ['hostname',],
            "failed": [('hostname', 'msg'), {}],
        }
        """
        result = {'success': [], 'failed': []}
        for host in self.results_callback.result_q['contacted']:
            result['success'].append(host)

        for host, msgs in self.results_callback.result_q['dark'].items():
            msg = '\n'.join(['{} {}: {}'.format(
                msg.get('module_stdout', ''),
                msg.get('invocation', {}).get('module_name'),
                msg.get('msg', '')) for msg in msgs])
            result['failed'].append((host, msg))
        return result