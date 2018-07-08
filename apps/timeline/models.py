# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from authority.models import ExtendUser
from execute.models import Callback
import uuid


class History(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExtendUser, blank=True, null=True, default=1, related_name='user',)
    type = models.IntegerField(default=0)#历史类型
    is_validated = models.BooleanField(default=False,)
    info = models.TextField(default='')#信息
    time = models.DateTimeField(auto_now_add=True,)#历史时间
