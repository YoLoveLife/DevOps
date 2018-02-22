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
                                                            label='')

    # user_name = forms.CharField(required=True,label=u'管理账户')
    # private_key = forms.FileField(required=True,label=u'私钥上传')
    # is_admin = forms.BooleanField(required=True,label=u'是否超管用户')
    sys_user = forms.ModelMultipleChoiceField(required=False,queryset=models.Sys_User.objects.all(),
                                              to_field_name='id',widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                              label='')
    class Meta:
        model = models.Group
        fields = ['name','info','framework','hosts','users','sys_user']
        widgets = {
            'info':forms.Textarea(attrs=None)
        }
        labels = {
            'framework':u'架构图',
            'name':u'应用组名称',
            'info':u'应用组信息'
        }

    def save_hosts_new(self):
        group = self.save()
        self.instance.hosts = self.cleaned_data['hosts']
        return group.save()

    def save_hosts_update(self):
        self.instance.hosts = self.cleaned_data['hosts']
        return self.save()

class HostBaseForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(required=False,queryset=models.Group.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label=u'应用组')
    storages = forms.ModelMultipleChoiceField(required=False,queryset=models.Storage.objects.all(),
                                                             to_field_name="id",widget=forms.SelectMultiple(attrs={'class':'select2'}),
                                                             label=u'存储')
    systemtype = forms.ModelChoiceField(required=True,queryset=models.System_Type.objects.all(),
                                        to_field_name="id",widget=forms.Select(attrs={'class':'select2'}),
                                        label=u'操作系统')
    connect_ip = forms.GenericIPAddressField(required=True,label=u"连接IP")
    service_ip = forms.GenericIPAddressField(required=False,label=u"服务IP")

    coreness = forms.CharField(required=False,max_length=5,label=u"CPU核数")
    memory = forms.CharField(required=False,max_length=7,label=u"内存大小")
    root_disk = forms.CharField(required=False,max_length=7,label=u"本地磁盘")

    server_position = forms.CharField(required=False,empty_value=u'未指定位置')
    hostname = forms.CharField(required=False,empty_value=u'localhost.localdomain')
    sshport = forms.IntegerField(required=True,label=u'连接端口')
    info = forms.CharField(widget=forms.Textarea(attrs=None),label=u'信息')

    class Meta:
        model = models.Host
        fields = ['groups','storages','systemtype','connect_ip','service_ip','coreness','memory','root_disk',
                  'server_position','hostname','sshport','info'
                  ]
    #
    #
    # def clean_sshpasswd(self):
    #     sshpasswd = self.cleaned_data['sshpasswd']
    #     if checkpass.checkPassword(sshpasswd):
    #         return aes.encrypt(sshpasswd)
    #     else:
    #         raise forms.ValidationError(u'密码复杂度不足')
    def save(self, commit=True):
        host = super(HostBaseForm, self).save(commit=commit)

    # def _save_m2m(self):
    #     super(HostBaseForm, self)._save_m2m()
    #     sys_user_name = self.cleaned_data['sys_user_name']
    #     sys_user_private = self.cleaned_data['sys_user_private_key']
    #     models.Sys_User()
    #     self.instance.sys_user =
    #     assets = self.cleaned_data['assets']
    #     self.instance.assets.clear()
    #     self.instance.assets.add(*tuple(assets))


class HostCreateForm(HostBaseForm):
    def clean_connect_ip(self):
        connect_ip = self.cleaned_data['connect_ip']
        return connect_ip

    def clean_storages(self):
        storages = self.cleaned_data['storages']
        return storages

    def clean_groups(self):
        groups = self.cleaned_data['groups']
        connect_ip = self.cleaned_data['connect_ip']
        for group in groups:
            if group.hosts.filter(connect_ip=connect_ip).exists() == True:
                raise forms.ValidationError(u'应用组 %s 中已经存在该主机'%(group.name))
        return groups


class HostUpdateForm(HostBaseForm):
    def clean_connect_ip(self):
        #判断在groups中是否存在该管理IP
        connect_ip = self.cleaned_data['connect_ip']
        return connect_ip

    def clean_storages(self):
        storages = self.cleaned_data['storages']
        return storages

    def clean_groups(self):
        groups = self.cleaned_data['groups']
        connect_ip = self.cleaned_data['connect_ip']
        own_id = self.instance.id
        for group in groups:
            if group.hosts.exclude(id=own_id).filter(connect_ip=connect_ip).exists() == True:
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