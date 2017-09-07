# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from validate.models import ExtendUser
# Create your models here.
class Script(models.Model):
    SCRIPT_STATUS=(
        (0,u'未完成'),
        (1,u'已完成'),
    )
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='noName')
    info=models.CharField(max_length=100,default="noUse")
    script=models.TextField(default='')
    author = models.ForeignKey(ExtendUser, default=1, related_name='suser')
    status=models.IntegerField(default=0,choices=SCRIPT_STATUS)

class ScriptArgs(models.Model):
    id=models.AutoField(primary_key=True)
    args_name=models.CharField(max_length=100,default='')
    args_value=models.CharField(max_length=100,default='')
    script=models.ForeignKey(Script,default=1,related_name='scriptargs')


class PlayBook(models.Model):
    PLAYBOOK_STATUS=(
        (0,u'未完成'),
        (1,u'已完成'),
    )
    SUDO_STATUS=(
        (0,u'不需要'),
        (1,u'需要')
    )
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='noName')
    author = models.ForeignKey(ExtendUser,default=1,related_name='puser')
    info = models.CharField(max_length=100,default='noUse')
    sort = models.IntegerField(default=0)
    sudo = models.IntegerField(default=1,choices=SUDO_STATUS)
    status = models.IntegerField(default=0,choices=PLAYBOOK_STATUS)

class Adhoc(models.Model):
    id = models.AutoField(primary_key=True)
    mudule = models.CharField(default='hostname',max_length=20)
    args = models.CharField(default='',max_length=100)
    sort = models.IntegerField(default=0)
    playbook = models.ForeignKey(PlayBook,default=1,related_name='adhocs')

