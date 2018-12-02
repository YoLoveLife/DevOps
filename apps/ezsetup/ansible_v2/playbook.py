# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from ansible.errors import AnsibleParserError,AnsibleUndefinedVariable
from django.conf import settings
from deveops.ansible_v2.playbook import Playbook
from ansible.playbook.play import Play

__all__ = [
    "EZSetupPlaybook"
]


class EZSetupPlaybook(Playbook):
    def __init__(self, group, key, callback, setup):
        self.setup = setup
        super(EZSetupPlaybook, self).__init__(group, key, callback)

    def import_task(self, play_source):
        super(EZSetupPlaybook, self).import_task(play_source)
        # self.play.append(
        #     Play().load(
        #         play_source,
        #         variable_manager=self.variable_manager,
        #         loader=self.loader
        #     )
        # )
        # print(self.play)

    def import_vars(self, vars_dict):
        try:
            super(EZSetupPlaybook, self).import_vars(vars_dict)
        except AnsibleUndefinedVariable as e:
            pass

    def run(self):
        try:
            super(EZSetupPlaybook, self).run()
        finally:
            self.setup.status = settings.STATUS_EZSETUP_DONE

