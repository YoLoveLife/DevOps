# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes,checkpass
from manager.models import System_Type
# class GroupCreateUpdateForm(forms.ModelForm):
#     class Meta:
#         model = models.System_Type
#         fields = ['name']
#         widgets = {
#             'name':forms.CharField(attrs=None)
#         }
#         labels = {
#             'name':'操作系统名称',
#         }

class JumperBaseForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(required=False,queryset=models.Group.objects.all(),
                                    to_field_name='id',widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                    label=u'应用组')

    class Meta:
        model = models.Jumper
        fields = ['connect_ip','sshport','info','groups']
        widgets = {
            'sshpasswd': forms.TextInput(attrs={'type':'password'}),
        }
        labels = {
            'connect_ip': u'连接IP',
            'sshport': u'访问端口',
            'info': u'信息',
        }

    def clean_sshpasswd(self):
        sshpasswd = self.cleaned_data['sshpasswd']
        if checkpass.checkPassword(sshpasswd):
            return aes.encrypt(sshpasswd)
        else:
            raise forms.ValidationError(u'密码复杂度不足')

class JumperCreateForm(JumperBaseForm):
    def clean_group(self):
        groups = self.cleaned_data['groups']
        for group in groups:
            if group.jumper.count() == 0:
                continue
            else:
                raise forms.ValidationError(u'应用组 %s 已经包含跳板机'%(group.name))
        return groups

class JumperUpdateForm(JumperBaseForm):
    def clean_group(self):
        groups = self.cleaned_data['groups']
        connect_ip = self.cleaned_data['connect_ip']
        for group in groups:
            if group.jumper is None:
                continue
            jumper = group.jumper.get()
            if jumper.connect_ip != connect_ip:
                raise forms.ValidationError(u'试图将新的跳板机写入完整的应用组')
        return groups


class SystemTypeForm(forms.ModelForm):
    class Meta:
        model = System_Type
        fields = ['name']
        labels = {
            'name': u'系统名称',
        }

    def clean_name(self):
        sub_name = self.cleaned_data['name']
        if System_Type.objects.filter(name=sub_name).count() ==0:
            return sub_name
        else:
            return 'null'

    # 重写基类函数 将原本的Form save内容注销掉
    def save(self, commit=True):
        if self.instance.name == 'null':
            print(self.instance.name)
            return None
        else:
            print(self.instance.name)
            return super(SystemTypeForm,self).save(commit=commit)