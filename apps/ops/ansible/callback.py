# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from ansible.plugins.callback import CallbackBase
from django.conf import settings
INDENT = 4


class AnsibleCallback(CallbackBase):

    def __init__(self, consumer, push_mission):
        self.consumer = consumer
        self.push_mission = push_mission
        return super(AnsibleCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        self.consumer.send('OK')
        # print('OK',self._dump_results(result._result, indent=INDENT)
        self.push_mission.status = settings.OPS_PUSH_MISSION_RUNNING
        self.push_mission.results_append(self._dump_results(result._result, indent=INDENT))

    def v2_runner_on_unreachable(self, result):
        self.consumer.send('UNREACHABLE')
        self.push_mission.status = settings.OPS_PUSH_MISSION_UNREACHABLE
        self.push_mission.results_append(self._dump_results(result._result, indent=INDENT))
        # print('UNREACHABLE', self._dump_results(result._result, indent=INDENT))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.consumer.send('FAILED')
        self.push_mission.status = settings.OPS_PUSH_MISSION_FAILED
        self.push_mission.results_append(self._dump_results(result._result, indent=INDENT))
        # print('FAILED', self._dump_results(result._result, indent=INDENT))


class JudgementCallback(AnsibleCallback):

    def __init__(self, consumer, push_mission):
        self.judgement = True
        return super(JudgementCallback, self).__init__(consumer,push_mission)

    def v2_runner_on_ok(self, result, **kwargs):
        r = self._dump_results(result._result, indent=INDENT)
        if r.has_key('stdout'):
            self.judgement = self.judgement and (r['stdout'] == "True" or r['stdout'] == "true")
        if self.judgement is not True:
            self.push_mission.status = settings.OPS_PUSH_MISSION_FAILED
