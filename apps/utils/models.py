# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import unicode_literals

from django.db import models

class System_Type(models.Model):
    id = models.AutoField(primary_key=True) #全局ID
    name = models.CharField(max_length=50,default="") #字符长度

    def __unicode__(self):
        return self.name