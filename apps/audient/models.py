# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import uuid
from django.db import models
from authority.models import ExtendUser

__all__ = [
    "Audient",
]


class Audient(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    channel = models.IntegerField(max_length=100, default='email')
    user = models.OneToOneField(ExtendUser, related_name='src_safe_work', on_delete=models.SET_NULL, null=True,
                                blank=True)

