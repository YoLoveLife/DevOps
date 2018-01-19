# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models

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
    group = forms.ModelChoiceField(required=True,queryset=models.Group.objects.all(),
                                    to_field_name='id',widget=forms.Select(attrs={'class':'select2'}),
                                    label=u'应用组')

    class Meta:
        model = models.Jumper
        fields = ['service_ip','normal_user','sshpasswd','sshport','info','group']
        labels = {
            'service_ip': u'服务IP',
            'normal_user': u'用户',
            'sshpasswd': u'密码',
            'sshport': u'访问端口',
            'info': u'信息',
        }

class JumperCreateForm(JumperBaseForm):
    def clean_group(self):
        group = self.cleaned_data['group']
        return group

class JumperUpdateForm(JumperBaseForm):
    def clean_group(self):
        group = self.cleaned_data['group']
        if group.jumper is not None:
            raise forms.ValidationError(u'该应用组已经存在跳板机')
        else:
            return group