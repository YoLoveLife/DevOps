# -*- coding:utf-8 -*-
from ansible.errors import AnsibleParserError,AnsibleUndefinedVariable
from django.conf import settings
from deveops.ansible.playbook import Playbook
from ansible.playbook.play import Play
__all__ = [
    "EZSetupPlaybook"
]

class EZSetupPlaybook(Playbook):
    def __init__(self, host_list, key, callback, setup):
        self.setup = setup
        super(EZSetupPlaybook, self).__init__(host_list, key, callback)

    def import_task(self, play_source):
        # super(EZSetupPlaybook, self).import_task([play_source])
        self.play.append(
            Play().load(
                play_source,
                variable_manager=self.variable_manager,
                loader=self.loader
            )
        )
        print(self.play)

    def import_vars(self, vars_dict):
        try:
            super(EZSetupPlaybook, self).import_vars(vars_dict)
        except AnsibleUndefinedVariable as e:
            pass

    def run(self):
        super(EZSetupPlaybook, self).run()


