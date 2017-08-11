# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _

class ScriptForm(forms.ModelForm):
    class Meta:
        model = models.Script
        fields = ['id','name','script','author','info']
        labels = {
            'id':'脚本ID','name':'脚本名称','script':'脚本内容','author':'脚本作者','info':'脚本信息'
        }
        widgets = {
            'id': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'yes'}),
            'script':forms.Textarea(attrs=None),
        }

class ScriptCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Script
        fields = ['name','script','author','info']
        labels = {
            'id':'脚本ID','name':'脚本名称','script':'脚本内容','author':'脚本作者','info':'脚本信息'
        }
        widgets = {
            'id': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'yes'}),
            'script':forms.Textarea(attrs=None),
        }