# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _
class GroupCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ['name','info']
        widgets = {
            'info':forms.Textarea(attrs=None)
        }
        labels = {
            'name':'应用组名称',
            'info':'应用组信息'
        }

class HostCreateUpdateForm(forms.ModelForm):
    manage_ip = forms.CharField(required=False,max_length=15,label="管理IP")
    outer_ip = forms.CharField(required=False,max_length=15,label="外网IP")
    coreness = forms.CharField(required=False,max_length=5,label="CPU核数")
    memory = forms.CharField(required=False,max_length=7,label="内存大小")
    root_disk = forms.CharField(required=False,max_length=7,label="本地磁盘")
    class Meta:
        model = models.Host
        fields = ['systemtype','manage_ip',
                  'service_ip','outer_ip','server_position',
                  'hostname','normal_user','sshport',
                  'coreness','memory','root_disk','info','sshpasswd']
        widgets = {
            'info':forms.Textarea(attrs=None),
            'systemtype': forms.Select(attrs={'type': 'select2 form-control'}),
            'sshpasswd': forms.TextInput(attrs={'type':'password'})
        }
        labels = {
            'systemtype':'操作系统','manage_ip':'管理IP','sshport':'管理端口',
            'service_ip':'服务IP','outer_ip':'外网IP','server_position':'服务器位置',
            'hostname':'主机名称','normal_user':'普通用户','coreness':'CPU核数',
            'memory':'内存大小','root_disk':'本地磁盘','info':'信息','sshpasswd':'管理密码'
        }

class StorageCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Storage
        fields = ['disk_path','disk_size','info']
        widgets = {
            'info':forms.Textarea(attrs=None),
        }
        labels = {
            'disk_size':'存储大小','disk_path':'存储路径','info':'信息'
        }