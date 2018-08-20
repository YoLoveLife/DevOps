# -*- coding:utf-8 -*-
from ansible.errors import AnsibleParserError,AnsibleUndefinedVariable
from django.conf import settings
from deveops.ansible_v2.playbook import Playbook
__all__ = [
    "DiskOverFlowPlaybook"
]

class DiskOverFlowPlaybook(Playbook):
    def __init__(self, group, key, callback):
        super(DiskOverFlowPlaybook, self).__init__(group, key, callback)

    def import_task(self, play_source):
        super(DiskOverFlowPlaybook, self).import_task(play_source)

    def import_vars(self, vars_dict):
        try:
            super(DiskOverFlowPlaybook, self).import_vars(vars_dict)
        except AnsibleUndefinedVariable as e:
            pass

    def run(self):
        super(DiskOverFlowPlaybook, self).run()

