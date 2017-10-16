import json
from .. import ResultCallback
class BasicResultCallback(ResultCallback):
    def __init__(self):
        super(BasicResultCallback,self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        super(BasicResultCallback,self).v2_runner_on_ok(result,**kwargs)

    def v2_runner_on_unreachable(self, result):
        super(BasicResultCallback,self).v2_runner_on_unreachable(result)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(BasicResultCallback,self).v2_runner_on_failed(result,ignore_errors)
