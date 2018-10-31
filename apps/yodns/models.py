# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-8-15
# Author Yo
# Modify WZZ
# Email YoLoveLife@outlook.com
import uuid
from django.db import models
from manager.models import Group

__all__ = [
    'DNS'
]

class DNS(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(Group, related_name='dns',
                              verbose_name="group", blank=True,
                              null=True, on_delete=models.SET_NULL,
                              help_text="所属应用组")

    internal_dig = models.CharField(max_length=100, default='', verbose_name='内网解析地址',help_text="内网解析地址", null=True, blank=True)
    external_dig = models.CharField(max_length=100, default='', verbose_name='外网解析地址',help_text="外网解析地址", null=True, blank=True)
    url = models.CharField(max_length=100, verbose_name="域名", help_text="域名", default='', )

    class Meta:
        permissions = (
            ('yo_list_dns', u'罗列域名'),
            ('yo_create_dns', u'新增域名'),
            ('yo_update_dns', u'修改域名'),
            ('yo_detail_dns', u'详细查看域名'),
            ('yo_delete_dns', u'删除域名'),
        )

