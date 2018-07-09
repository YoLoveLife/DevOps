from django.db import models
from authority.models import ExtendUser
import uuid

class History(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExtendUser, blank=True, null=True, default=1, related_name='user', on_delete=models.SET_NULL)
    type = models.IntegerField(default=0)#历史类型
    is_validated = models.BooleanField(default=False,)
    info = models.TextField(default='')#信息
    time = models.DateTimeField(auto_now_add=True,)#历史时间
