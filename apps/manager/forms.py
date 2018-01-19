# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes,checkpass
from django.utils.translation import gettext_lazy as _

class GroupCreateUpdateForm(forms.ModelForm):
    hosts = forms.ModelMultipleChoiceField(required=False,queryset=models.Host.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label='')
    users = forms.ModelMultipleChoiceField(required=False,queryset=models.ExtendUser.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label='用户')
    class Meta:
        model = models.Group
        fields = ['name','info','framework','hosts','users']
        widgets = {
            'info':forms.Textarea(attrs=None)
        }
        labels = {
            'name':'应用组名称',
            'info':'应用组信息'
        }

    def save_hosts_new(self):
        group = self.save()
        self.instance.hosts = self.cleaned_data['hosts']
        return group.save()

    def save_hosts_update(self):
        self.instance.hosts = self.cleaned_data['hosts']
        return self.save()

class HostBaseForm(forms.ModelForm):
    # status = forms.CharField(required=True,disabled=True)
    manage_ip = forms.CharField(required=False,max_length=15,label=u"管理IP")
    outer_ip = forms.CharField(required=False,max_length=15,label=u"外网IP")
    coreness = forms.CharField(required=False,max_length=5,label=u"CPU核数")
    memory = forms.CharField(required=False,max_length=7,label=u"内存大小")
    root_disk = forms.CharField(required=False,max_length=7,label=u"本地磁盘")
    service_ip = forms.CharField(required=True,max_length=15,label=u"服务IP")
    groups = forms.ModelMultipleChoiceField(required=False,queryset=models.Group.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label=u'应用组')
    storages = forms.ModelMultipleChoiceField(required=False,queryset=models.Storage.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label=u'存储')
    systemtype = forms.ModelChoiceField(required=True,queryset=models.System_Type.objects.all(),
                                        to_field_name="id",widget=forms.Select(attrs={'class':'select2'}),
                                        label=u'操作系统')
    class Meta:
        model = models.Host
        fields = ['systemtype','manage_ip',
                  'service_ip','outer_ip','server_position',
                  'hostname','normal_user','sshport',
                  'coreness','memory','root_disk','info','sshpasswd',
                  'storages','groups',
                  ]
        widgets = {
            'info':forms.Textarea(attrs=None),
            'sshpasswd': forms.TextInput(attrs={'type':'password'}),
        }
        labels = {
            'sshport':'管理端口',
            'server_position':'服务器位置',
            'hostname':'主机名称','normal_user':'普通用户',
            'info':'信息','sshpasswd':'管理密码',
        }
    def clean_sshpasswd(self):
        sshpasswd = self.cleaned_data['sshpasswd']
        if checkpass.checkPassword(sshpasswd):
            return aes.encrypt(sshpasswd)
        else:
            raise forms.ValidationError(u'密码复杂度不足')

class HostCreateForm(HostBaseForm):
    def clean_service_ip(self):
        service_ip = self.cleaned_data['service_ip']
        return service_ip

    def clean_storages(self):
        storages = self.cleaned_data['storages']
        return storages

    def clean_groups(self):
        groups = self.cleaned_data['groups']
        service_ip = self.cleaned_data['service_ip']
        for group in groups:
            if group.hosts.filter(service_ip=service_ip).exists() == True:
                raise forms.ValidationError(u'应用组 %s 中已经存在该主机'%(group.name))
        return groups


class HostUpdateForm(HostBaseForm):
    def clean_service_ip(self):
        #判断在groups中是否存在该管理IP
        service_ip = self.cleaned_data['service_ip']
        return service_ip

    def clean_storages(self):
        storages = self.cleaned_data['storages']
        return storages

    def clean_groups(self):
        groups = self.cleaned_data['groups']
        service_ip = self.cleaned_data['service_ip']
        own_id = self.instance.id
        for group in groups:
            if group.hosts.exclude(id=own_id).filter(service_ip=service_ip).exists() == True:
                raise forms.ValidationError(u'应用组 %s 中已经存在该主机' % (group.name))
        return groups


class StorageCreateUpdateForm(forms.ModelForm):
    hosts = forms.ModelMultipleChoiceField(required=False,queryset=models.Host.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label='')
    class Meta:
        model = models.Storage
        fields = ['disk_path','disk_size','info','hosts']
        widgets = {
            'info':forms.Textarea(attrs=None),
        }
        labels = {
            'disk_size':'存储大小','disk_path':'存储路径','info':'信息'
        }

    def save_hosts_new(self):
        storage = self.save()
        self.instance.hosts = self.cleaned_data['hosts']
        return storage.save()

    def save_hosts_update(self):
        self.instance.hosts = self.cleaned_data['hosts']
        return self.save()