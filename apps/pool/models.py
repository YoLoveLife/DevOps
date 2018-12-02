# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid

__all__ = [
    "IP_Pool",
]

class IP_Pool(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    A_address = models.CharField(default='127', max_length=3)
    B_address = models.CharField(default='0', max_length=3)
    C_address = models.CharField(default='0', max_length=3)
    D_address = models.CharField(default='1', max_length=3)

    type = models.IntegerField(default=0)
    info = models.CharField(default='', max_length=500)

    @property
    def ip_address(self):
        return '.'.join(
            [
                self.A_address,
                self.B_address,
                self.C_address,
                self.D_address,
            ]
        )