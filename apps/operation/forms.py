# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models

class ScriptCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Script
        # fields = ['name','script','author','info']
        fields = ['script','name','info']
        labels = {
            'script':'脚本内容','info':'脚本信息','name':'脚本名称',
        }
        widgets = {
            'script':forms.Textarea(attrs={'style':'height:500px;','class':'summernote'}),
        }

class ScriptArgsCreateUpdateForm(forms.ModelForm):
    class Meta:
            model = models.ScriptArgs
            fields = ['args_name', 'args_value']
            labels = {
                'args_name': '参数名称',
                'args_value': '参数默认数值'
            }
            widgets = {
                'args_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
                'args_value': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
            }

class PlaybookCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.PlayBook
        fields = ['name','info']
        labels = {
            'info':'脚本信息','name':'脚本名称',
        }
        widgets = {
        }