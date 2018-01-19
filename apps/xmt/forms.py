# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _
class XMTForm(forms.ModelForm):
    class Meta:
        model = models.XMT
        fields = ['name','env','model','gitlab']
        widgets = {
            'name': forms.Select(attrs={'type': 'select2 form-control'}),
            'env': forms.Select(attrs={'type': 'select2 form-control'}),
            'model': forms.Select(attrs={'type': 'select2 form-control'}),
        }
        labels = {
            'name':'操作人','env':'环境','model':'模块','gitlab':'版本编号'
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        print(name)
        if name == 0:
            raise forms.ValidationError(u'未选择更新人')
        return name

    def clean_model(self):
        model = self.cleaned_data['model']
        print(model)
        if model == 0:
            raise forms.ValidationError(u'未选择更新模块')
        return model

    def clean_env(self):
        env = self.cleaned_data['env']
        print(env)
        if env == 0:
            raise forms.ValidationError(u'未选择更新环境')
        return env

    def clean_gitlab(self):
        gitlab = self.cleaned_data['gitlab']
        print(gitlab)
        if gitlab != 'null':
            raise forms.ValidationError(u'您更新了非最新代码')
        return gitlab