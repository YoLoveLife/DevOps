# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
from django.utils.translation import gettext_lazy as _
from authority.models import ExtendUser,Permission,Group
#__all__ = ['UserCreateUpdateForm']
class UserCreateUpdateForm(forms.ModelForm):
    # is_active = forms.IntegerField(required=True)
    email = forms.CharField(required=True,max_length=15,label='电子邮箱',help_text=_('必填. 请输入8531集团邮箱'),)
    first_name = forms.CharField(required=True,max_length=15,label='姓')
    last_name = forms.CharField(required=True,max_length=15,label='名')
    phone = forms.CharField(required=True,max_length=15,label='电话号码',help_text=_('必填. 请填写正确的手机号码'),)
    class Meta:
        model = ExtendUser
        fields = ['username','first_name','last_name','email','phone'] #'is_active'
        labels = {
            'username':'登陆账户',
            'first_name':'姓',
            'last_name':'名',
            'email':'邮箱',
            # 'is_active':'是否通行',
            'phone':'电话号码',
        }

    def before_save(self,request,commit):
        auths_id_list = request.POST.getlist('auths', [])
        auths = Group.objects.filter(id__in=auths_id_list)
        exuser = self.save(commit=commit)
        exuser.groups.clear()
        exuser.groups.add(*auths)
        is_active = request.POST.get('is_active')
        if is_active == 'actived':
            exuser.is_active = True
        else:
            exuser.is_active = False

class AuthGroupCreateUpdate(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def before_save(self,request,commit):
        auth_id_list = self.request.POST.getlist('auths', [])
        auths = Permission.objects.filter(id__in=auth_id_list)
        self.permissions.add(*auths)