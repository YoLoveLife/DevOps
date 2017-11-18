# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _
#__all__ = ['DBCreateUpdateForm']
class DBCreateUpdateForm(forms.ModelForm):
    service_ip = forms.CharField(required=True,max_length=13,label='业务IP')
    class Meta:
        model = models.DB
        fields = ['prefix','root_passwd',
                  'port','socket','datadir','service_ip']
        widgets = {
            'root_passwd': forms.TextInput(attrs={'type':'password'})
        }
        labels = {
            'prefix':'prefix','root_passwd':'管理密码','port':'服务端口',
            'socket':'Socket','datadir':'数据目录',
        }