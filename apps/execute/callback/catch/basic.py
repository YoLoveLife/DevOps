import json

from timeline.models import History
from execute.models import Callback
from .. import ResultCallback

class BasicResultCallback(ResultCallback):
    def v2_runner_on_ok(self, result, **kwargs):
        c = Callback()
        c.info=json.dumps(result._result)
        c.history = History.objects.get(id=1)
        c.save()
        return c.id