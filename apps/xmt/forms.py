# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _
class XMTForm(forms.ModelForm):
    user = forms.ModelChoiceField(required=False,queryset=models.ExtendUser.objects.all(),
                                                             to_field_name="id",widget=forms.Select(attrs={'style':'display:none'}),
                                                             label='',disabled=True)
    gitlab = forms.CharField(required=True,initial='null',disabled=True,label='版本编号')
    class Meta:
        model = models.XMT
        fields = ['env','gitlab','model','info','user']
        widgets = {
            'env': forms.Select(attrs={'type': 'select2 form-control'}),
            'model': forms.Select(attrs={'type': 'select2 form-control'}),
        }
        labels = {
            'env':'环境','model':'模块','info':'更新内容'
        }

    def clean_user(self):
        return self.user

    def clean_model(self):
        model = self.cleaned_data['model']
        return model

    def clean_env(self):
        env = self.cleaned_data['env']
        if env == 0:
            raise forms.ValidationError(u'未选择更新环境')

        if env == 2 and (self.user.is_superuser or self.user.is_oper):
            pass
        elif env == 2:
            raise forms.ValidationError(u'开发人员无法更新生产环境')
        return env

    def clean_gitlab(self):
        gitlab = self.cleaned_data['gitlab']
        if gitlab != 'null':
            raise forms.ValidationError(u'您更新了非最新代码')
        return gitlab