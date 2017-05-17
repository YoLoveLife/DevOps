from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField()
    password=models.CharField(max_length=64)