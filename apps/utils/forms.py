# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes,checkpass
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
        fields = ['service_ip','normal_user','sshpasswd','sshport','info','groups']
        widgets = {
            'sshpasswd': forms.TextInput(attrs={'type':'password'}),
        }
        labels = {
            'service_ip': u'服务IP',
            'normal_user': u'用户',
            'sshpasswd': u'密码',
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
        service_ip = self.cleaned_data['service_ip']
        for group in groups:
            if group.jumper is None:
                continue
            jumper = group.jumper.get()
            if jumper.service_ip != service_ip:
                raise forms.ValidationErroru(u'试图将新的跳板机写入完整的应用组')
        return groups