# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from ansible.plugins.callback import CallbackBase
INDENT = 4


class AnsibleCallback(CallbackBase):

    def __init__(self, replay_name):
        self.replay_name = replay_name
        return super(AnsibleCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        from deveops.asgi import channel_layer
        message = "{host} => SUCCESS\r\n".format(host=result._host.get_name())
        channel_layer.send(self.replay_name,
                           {'text': message})
        channel_layer.send(self.replay_name, {'text':self._dump_results(result._result,indent=INDENT).replace('\n','\r\n')+'\r\n'})


    def v2_runner_on_unreachable(self, result):
        from deveops.asgi import channel_layer
        message = "{host} => UNREACHABLE!\r\n".format(host=result._host.get_name())
        channel_layer.send(self.replay_name, {'text': message})
        channel_layer.send(self.replay_name,
                           {'text': self._dump_results(result._result, indent=INDENT).replace('\n', '\r\n') + '\r\n'})


    def v2_runner_on_failed(self, result, ignore_errors=False):
        from deveops.asgi import channel_layer
        message = "{host} => FAILED!\r\n".format(host=result._host.get_name())

        channel_layer.send(self.replay_name, {'text': message})
        channel_layer.send(self.replay_name, {'text': self._dump_results(result._result, indent=INDENT)})
