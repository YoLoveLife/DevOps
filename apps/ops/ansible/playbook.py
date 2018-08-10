# -*- coding:utf-8 -*-
from ansible.errors import AnsibleParserError,AnsibleUndefinedVariable
from django.conf import settings
from deveops.ansible.playbook import Playbook

__all__ = [
    "OpsPlaybook"
]

class OpsPlaybook(Playbook):
    def __init__(self, host_list, key, callback, consumer, push_mission):
        super(OpsPlaybook, self).__init__(host_list, key, callback)
        self.consumer = consumer
        self.push_mission = push_mission

    def import_vars(self, vars_dict):
        self.push_mission.status = settings.OPS_PUSH_MISSION_IMPORT_VAR
        try:
            super(OpsPlaybook, self).import_vars(vars_dict)
            self.push_mission.results_append('参数载入成功;')
            self.push_mission.results_append(vars_dict)
        except AnsibleUndefinedVariable as e:
            self.push_mission.results_append('参数识别失败;')
            self.consumer.send('ERROR')
            self.consumer.close()
        self.consumer.send('OK')


    def import_task(self, play_source):
        self.push_mission.status = settings.OPS_PUSH_MISSION_IMPORT_TASKS
        try:
            self.push_mission.results_append(play_source)
            super(OpsPlaybook, self).import_task(play_source)
            self.push_mission.results_append('任务载入成功;')
        except AnsibleParserError as e:
            self.push_mission.results_append('错误或者丢失模块;')
            self.consumer.send('ERROR')
            self.consumer.close()
        self.consumer.send('OK')

    def run(self):
        super(OpsPlaybook, self).run()
        self.push_mission.status = settings.OPS_PUSH_MISSION_SUCCESS
        self.consumer.send("SUCCESS")


