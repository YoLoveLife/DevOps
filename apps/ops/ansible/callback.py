# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf import settings
from deveops.ansible.callback import Callback
INDENT = 4


class OpsCallback(Callback):
    def __init__(self, consumer, push_mission):
        self.consumer = consumer
        self.push_mission = push_mission
        super(OpsCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        super(OpsCallback, self).v2_runner_on_ok(result, **kwargs)
        self.consumer.send('OK')
        self.push_mission.status = settings.OPS_PUSH_MISSION_RUNNING
        self.push_mission.results_append(self._dump_results(result._result, indent=INDENT))

    def v2_runner_on_unreachable(self, result):
        super(OpsCallback, self).v2_runner_on_unreachable(result)
        self.consumer.send('UNREACHABLE')
        self.push_mission.status = settings.OPS_PUSH_MISSION_UNREACHABLE
        self.push_mission.results_append(self._dump_results(result._result, indent=INDENT))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(OpsCallback, self).v2_runner_on_failed(result, ignore_errors)
        self.consumer.send('FAILED')
        self.push_mission.status = settings.OPS_PUSH_MISSION_FAILED
        self.push_mission.results_append(self._dump_results(result._result, indent=INDENT))