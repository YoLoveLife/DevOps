# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf import settings
from deveops.ansible_v2.callback import Callback
INDENT = 4

class DiskOverFlowCallback(Callback):
    def __init__(self):
        super(DiskOverFlowCallback, self).__init__()


    def v2_runner_on_ok(self, result, **kwargs):
        percentage = result._result['stdout']
        print(percentage)
        if int(percentage[:-1]) > settings.DISK_LIMIT:
            print(123)
        super(DiskOverFlowCallback, self).v2_runner_on_ok(result, **kwargs)


    def v2_runner_on_unreachable(self, result):
        super(DiskOverFlowCallback, self).v2_runner_on_unreachable(result)


    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(DiskOverFlowCallback, self).v2_runner_on_failed(result, ignore_errors)