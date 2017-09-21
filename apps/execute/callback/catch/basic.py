import json

from timeline.models import History
from execute.models import Callback
from .. import ResultCallback

class BasicResultCallback(ResultCallback):
    def v2_runner_on_ok(self, result, **kwargs):
        c = Callback()
        c.info=json.dumps(result._result)
        self.result = result._result
        c.save()
        self.c = c
        return

    def ResultExtract(self):
        return self.result['stdout_lines']