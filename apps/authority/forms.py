# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
from django.utils.translation import gettext_lazy as _
from validate.models import ExtendUser
#__all__ = ['UserCreateUpdateForm']
class UserCreateUpdateForm(forms.ModelForm):
    email = forms.CharField(required=True,max_length=15,label='电子邮箱',help_text=_('必填. 请输入8531集团邮箱'),)
    first_name = forms.CharField(required=True,max_length=15,label='姓')
    last_name = forms.CharField(required=True,max_length=15,label='名')
    phone = forms.CharField(required=True,max_length=15,label='电话号码',help_text=_('必填. 请填写正确的手机号码'),)
    class Meta:
        model = ExtendUser
        fields = ['username','first_name','last_name','email','is_active','phone']
        labels = {
            'username':'登陆账户',
            'first_name':'姓',
            'last_name':'名',
            'email':'邮箱',
            'is_active':'是否通行',
            'phone':'电话号码',
        }