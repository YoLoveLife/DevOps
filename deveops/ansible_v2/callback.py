# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
from ansible.plugins.callback import CallbackBase

class Callback(CallbackBase):
    def __init__(self):
        super(Callback,self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        return super(Callback, self).v2_runner_on_ok(result)

    def v2_runner_on_unreachable(self, result):
        return super(Callback, self).v2_runner_on_unreachable(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        return super(Callback, self).v2_runner_on_failed(result, ignore_errors)