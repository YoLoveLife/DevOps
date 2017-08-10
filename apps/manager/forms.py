# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ['id','name','info']
        labels = {
            'id':'应用ID','name':'应用组名称','info':'应用组信息'
        }
        widgets = {
            'id':forms.TextInput(attrs={'type':'text','class':'form-control','readonly':'yes'}),
            'name':forms.TextInput(attrs={'type':'text','class':'form-control'}),
            'info':forms.TextInput(attrs={'type':'text','class':'form-control'})
        }
    # id=forms.IntegerField(label="ID",widget=forms.TextInput(attrs={'type':'text','class':'form-control','readonly':'yes'}))
    # name=forms.CharField(label="Name",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}),error_messages={'msg':'姓名错误'})
    # info=forms.CharField(label="Info",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}),error_messages={'msg':'信息错误'})


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
    manage_ip = forms.CharField(required=False,max_length=15)
    outer_ip = forms.CharField(required=False,max_length=15)
    coreness = forms.CharField(required=False,max_length=5)
    memory = forms.CharField(required=False,max_length=7)
    root_disk = forms.CharField(required=False,max_length=7)
    class Meta:
        model = models.Host
        fields = ['systemtype','manage_ip',
                  'service_ip','outer_ip','server_position',
                  'hostname','normal_user','sshport',
                  'coreness','memory','root_disk','info']
        widgets = {
            'info':forms.Textarea(attrs=None),
            'systemtype': forms.Select(attrs={'type': 'select2 form-control'})
        }
        labels = {
            'systemtype':'操作系统','manage_ip':'管理IP','sshport':'管理端口',
            'service_ip':'服务IP','outer_ip':'外网IP','server_position':'服务器位置',
            'hostname':'主机名称','normal_user':'普通用户','coreness':'CPU核数',
            'memory':'内存大小','root_disk':'本地磁盘','info':'信息'
        }



class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = ['groups','storages','systemtype',
                 'manage_ip','service_ip','outer_ip',
                 'server_position','hostname','normal_user',
                 'sshpasswd','sshport','coreness','memory','root_disk','info']
        widgets = {
            'storages':forms.SelectMultiple(
                attrs={'class':'select2',
                       'data-placeholder':_('Select host storages')}),
            'groups':forms.SelectMultiple(
                attrs={'class':'select2',
                       'data-placeholder':_('Select host groups')}),
            'sshpasswd':forms.TextInput(attrs={'type':'password'}),
        }
        labels = {
            'systemtype':'操作系统','manage_ip':'管理IP','sshport':'管理端口','groups':'应用组',
            'service_ip':'服务IP','outer_ip':'外网IP','server_position':'服务器位置',
            'hostname':'主机名称','normal_user':'普通用户','sshpasswd':'用户密码',
            'coreness':'CPU核数','memory':'内存大小','root_disk':'本地磁盘',
            'storages':'存储选择','info':'信息'
        }


class StorageForm(forms.Form):
    id = forms.IntegerField(label="ID",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'yes'}))
    disk_size = forms.CharField(label="DiskSize", max_length=15,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    disk_path = forms.CharField(label="DiskPath", max_length=100,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    info = forms.CharField(label="Info", max_length=15,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))


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