# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from ansible.plugins.callback import CallbackBase
INDENT = 4


class AnsibleCallback(CallbackBase):

    def __init__(self, consumer, push_mission):
        self.consumer = consumer
        self.push_mission = push_mission
        return super(AnsibleCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        message = "{host} => SUCCESS\r\n".format(host=result._host.get_name())
        self.consumer.send(message)
        self.consumer.send(self._dump_results(result._result,indent=INDENT).replace('\n','\r\n')+'\r\n')

        self.push_mission.results = self.push_mission.results + self._dump_results(result._result)
        self.push_mission.save()

    def v2_runner_on_unreachable(self, result):
        message = "{host} => UNREACHABLE!\r\n".format(host=result._host.get_name())
        self.consumer.send(message)
        self.consumer.send(self._dump_results(result._result, indent=INDENT).replace('\n', '\r\n') + '\r\n')

        self.push_mission.results = self.push_mission.results + self._dump_results(result._result)
        self.push_mission.save()

    def v2_runner_on_failed(self, result, ignore_errors=False):
        message = "{host} => FAILED!\r\n".format(host=result._host.get_name())

        self.consumer.send(message)
        self.consumer.send(self._dump_results(result._result, indent=INDENT))
        self.push_mission.results = self.push_mission.results + self._dump_results(result._result)
        self.push_mission.save()

