# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Script(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='noName')
    info=models.CharField(max_length=100,default="noUse")
    script=models.TextField(default='')
    author=models.CharField(max_length=100,default='noAuthor')

class ScriptArgs(models.Model):
    id=models.AutoField(primary_key=True)
    args_name=models.CharField(max_length=100,default='')
    args_value=models.CharField(max_length=100,default='')
    script=models.ForeignKey(Script,default=1,related_name='scriptargs')

#
# class Playbook(models.Model):
#     id=models.AutoField(primary_key=True)