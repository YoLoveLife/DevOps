# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-7
# Author Yo
# Email YoLoveLife@outlook.com
import time
from collections import namedtuple

import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.utils.vars import load_extra_vars
from ansible.utils.vars import load_options_vars
from ansible.vars import VariableManager
from apps.execute.ansible.inventory import YoInventory
import os,glob
from operation.models import Script
FILENAME = r"/tmp/%s%s"
#__all__ = ['YoRunner']
class YoRunner(object):
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
        # self.variable_manager.extra_vars = load_extra_vars(self.loader,
        #                                                    options=self.options)
        self.variable_manager.extra_vars = extra_vars
        self.variable_manager.options_vars = load_options_vars(self.options)
        self.passwords = passwords or {}
        self.inventory = YoInventory(hosts)
        self.variable_manager.set_inventory(self.inventory)
        self.tasks = []
        self.play_source = None
        self.play = None
        self.runner = None
        self.timestamp = str(time.time())
        self.filename = FILENAME%(self.timestamp,'')
        self.have_script = 0

    def set_callback(self,callback):
        self.results_callback=callback

    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '%s' module." % module_name
            print(err)
            return False
        return True

    def task_add(self,task_tuple):
        for task in task_tuple:
            if not self.check_module_args(task.module,task.args):
                return
            if task.module == u'script':
                self.have_script = 1
                script = Script.objects.filter(id=task.args)
                if os.path.exists(self.filename):
                    os.remove(self.filename)
                script_name = FILENAME % (self.timestamp, '-' + str(script.get().id))
                output = open(script_name, 'w')
                output.writelines(script.get().formatScript())
                output.close()
            if self.have_script == 1:
                self.tasks.append(
                    dict(action=dict(
                        module=task.module,
                        args=script_name,
                    ))
                )
            else:
                self.tasks.append(
                    dict(action=dict(
                        module=task.module,
                        args=task.args,
                    ))
                )


    def run(self, task_tuple,):# pattern='all'):
        """
        :param task_tuple:  (('shell', 'ls'), ('ping', ''))
        :param pattern:
        :param timestamp:
        :return:
        """
        self.task_add(task_tuple)

        self.play_source = dict(
            name=self.timestamp,
            hosts='all',
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
            if self.have_script:
                self.cleanup_script()

    def cleanup_script(self):
        # if os.path.exists(self.filename):
        #     os.remove(self.filename)
        # return self.filename
        for name in glob.glob(self.filename+'*'):
            if os.path.exists(name):
                print(name)
                os.remove(name)
    # def clean_result(self):
    #     """
    #     :return: {
    #         "success": ['hostname',],
    #         "failed": [('hostname', 'msg'), {}],
    #     }
    #     """
    #     result = {'success': [], 'failed': []}
    #     for host in self.results_callback.result_q['contacted']:
    #         result['success'].append(host)
    #
    #     for host, msgs in self.results_callback.result_q['dark'].items():
    #         msg = '\n'.join(['{} {}: {}'.format(
    #             msg.get('module_stdout', ''),
    #             msg.get('invocation', {}).get('module_name'),
    #             msg.get('msg', '')) for msg in msgs])
    #         result['failed'].append((host, msg))
    #     return result