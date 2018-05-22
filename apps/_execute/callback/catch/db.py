# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-9
# Author Yo
# Email YoLoveLife@outlook.com

import json

from timeline.models import History
from execute.models import Callback
from .. import ResultCallback

class DBResultCallback(ResultCallback):
    def v2_runner_on_ok(self, result, **kwargs):
        c = Callback()
        c.info=json.dumps(result._result)
        self.result = result._result
        c.save()
        self.c = c
        self.status=1
        return super(DBResultCallback,self).v2_runner_on_ok(result,**kwargs)

    def v2_runner_on_unreachable(self, result):
        c = Callback()
        c.info=json.dumps(result._result)
        self.result = result._result
        c.save()
        self.c = c
        self.status=2
        return super(DBResultCallback,self).v2_runner_on_unreachable(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        c = Callback()
        c.info=json.dumps(result._result)
        self.result = result._result
        c.save()
        self.c = c
        self.status=0
        return super(DBResultCallback,self).v2_runner_on_failed(result,ignore_errors)

    def ResultExtract(self):
        return self.result['stdout_lines']