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
        fields = ['id','name','script','info']
        labels = {
            'id':'脚本ID','name':'脚本名称','script':'脚本内容','info':'脚本信息'
        }
        widgets = {
            'id': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'yes'}),
            'script':forms.Textarea(attrs=None),
        }

class ScriptCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Script
        # fields = ['name','script','author','info']
        fields = ['script']
        labels = {
            'script':'脚本内容'
        }
        widgets = {
            'script':forms.Textarea(attrs={'style':'height:500px;','class':'summernote'}),
        }

class ScriptArgsCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.ScriptArgs
        fields = ['args_name','args_value']
        labels = {
            'args_name':'参数名称',
            'args_value':'参数默认数值'
        }
        widgets = {
            'args_name':forms.TextInput(attrs={'type':'text','class':'form-control'}),
            'args_value':forms.TextInput(attrs={'type':'text','class':'form-control'} )
        }