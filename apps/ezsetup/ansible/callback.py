# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf import settings
from deveops.ansible.callback import Callback
INDENT = 4

class EZSetupCallback(Callback):
    def __init__(self, setup):
        self.setup = setup
        super(EZSetupCallback, self).__init__()


    def v2_runner_on_ok(self, result, **kwargs):
        super(EZSetupCallback, self).v2_runner_on_ok(result, **kwargs)


    def v2_runner_on_unreachable(self, result):
        super(EZSetupCallback, self).v2_runner_on_unreachable(result)


    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(EZSetupCallback, self).v2_runner_on_failed(result, ignore_errors)