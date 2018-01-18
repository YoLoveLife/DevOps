# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models

class GroupCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.System_Type
        fields = ['name']
        widgets = {
            'name':forms.CharField(attrs=None)
        }
        labels = {
            'name':'操作系统名称',
        }