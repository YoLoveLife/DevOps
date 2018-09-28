from django.db import models
from authority.models import ExtendUser
import uuid

class History(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField(default=0)#历史类型
    msg = models.TextField(default='')#信息
    time = models.DateTimeField(auto_now_add=True,)#历史时间
