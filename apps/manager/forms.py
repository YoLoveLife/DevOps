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
    class Meta:
        model = models.Group
        fields = ['name','info','framework']
        widgets = {
            'info':forms.Textarea(attrs=None)
        }
        labels = {
            'name':'应用组名称',
            'info':'应用组信息'
        }


    def before_save(self,request,commit):
        hosts_id_list = request.POST.getlist('hosts',[])
        hosts = models.Host.objects.filter(id__in=hosts_id_list)

        users_id_list = request.POST.getlist('users',[])
        users = models.ExtendUser.objects.filter(id__in=users_id_list)

        group = self.save(commit=commit)
        group.hosts.clear()
        group.hosts.add(*hosts)
        group.users.clear()
        group.users.add(*users)
        group.save()
        return group

class HostBaseForm(forms.ModelForm):
    # status = forms.CharField(required=True,disabled=True)
    manage_ip = forms.CharField(required=False,max_length=15,label="管理IP")
    outer_ip = forms.CharField(required=False,max_length=15,label="外网IP")
    coreness = forms.CharField(required=False,max_length=5,label="CPU核数")
    memory = forms.CharField(required=False,max_length=7,label="内存大小")
    root_disk = forms.CharField(required=False,max_length=7,label="本地磁盘")
    service_ip = forms.CharField(required=True,max_length=15,label="服务IP")
    groups = forms.ModelMultipleChoiceField(required=True,queryset=models.Group.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label='应用组')
    storages = forms.ModelMultipleChoiceField(required=True,queryset=models.Storage.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label='存储')
    class Meta:
        model = models.Host
        fields = ['systemtype','manage_ip',
                  'service_ip','outer_ip','server_position',
                  'hostname','normal_user','sshport',
                  'coreness','memory','root_disk','info','sshpasswd',
                  'groups','storages']
        widgets = {
            'info':forms.Textarea(attrs=None),
            'systemtype': forms.Select(attrs={'type': 'select2 form-control'}),
            'sshpasswd': forms.TextInput(attrs={'type':'password'}),
        }
        labels = {
            'systemtype':'操作系统','manage_ip':'管理IP','sshport':'管理端口',
            'outer_ip':'外网IP','server_position':'服务器位置',
            'hostname':'主机名称','normal_user':'普通用户','coreness':'CPU核数',
            'memory':'内存大小','root_disk':'本地磁盘','info':'信息','sshpasswd':'管理密码',
        }

    def clean_sshpasswd(self):
        sshpasswd = self.cleaned_data['sshpasswd']
        if checkpass.checkPassword(sshpasswd):
            return aes.encrypt(sshpasswd)
        else:
            raise forms.ValidationError(u'密码复杂度不足')

    def clean_service_ip(self):
        pass

class HostCreateForm(HostBaseForm):
    def clean_service_ip(self):
        service_ip = self.cleaned_data['service_ip']
        if models.Host.objects.filter(service_ip=service_ip).exists() == True:
            raise forms.ValidationError(u'该主机已经存在')
        return service_ip

class HostUpdateForm(HostBaseForm):
    def clean_service_ip(self):
        service_ip = self.cleaned_data['service_ip']
        return service_ip

class StorageCreateUpdateForm(forms.ModelForm):
    hosts = forms.ModelMultipleChoiceField(required=True,queryset=models.Host.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label='用户')
    class Meta:
        model = models.Storage
        fields = ['disk_path','disk_size','info','hosts']
        widgets = {
            'info':forms.Textarea(attrs=None),
        }
        labels = {
            'disk_size':'存储大小','disk_path':'存储路径','info':'信息'
        }

    def _save_m2m(self):
        super(StorageCreateUpdateForm,self)._save_m2m()
        hosts = self.cleaned_data['hosts']
        self.instance.hosts.clear()
        self.instance.hosts.add(*tuple(hosts))
    #
    # def clean_hosts(self):
    #
    # def before_save(self,request,commit):
    #     hosts_id_list=request.POST.getlist('hosts',[])
    #     hosts = models.Host.objects.filter(id__in=hosts_id_list)
    #     storage = self.save()
    #     storage.hosts.clear()
    #     storage.hosts.add(*hosts)
    #     return self.save()