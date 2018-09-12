# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid
from authority.models import ExtendUser

__all__ = [
]


class Audient(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    channel = models.IntegerField(max_length=100, default='email')
    user = models.OneToOneField(ExtendUser, related_name='src_safe_work', on_delete=models.SET_NULL, null=True, blank=True)