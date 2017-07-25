# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.contrib.auth.forms import AuthenticationForm


class GroupForm(forms.Form):
    id=forms.IntegerField(label="ID",widget=forms.TextInput(attrs={'type':'text','class':'form-control','readonly':'yes'}))
    name=forms.CharField(label="Name",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}),error_messages={'msg':'姓名错误'})
    info=forms.CharField(label="Info",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}),error_messages={'msg':'信息错误'})

    def is_valid(self):
        if self.data['name'] != "" and self.data['info'] != "" :
            return True
        else:
            return False

    def clean(self):
        is_name_exist=models.Group.objects.filter(name=self.data['name']).exists()
        if is_name_exist:
            return {'success':False,'msg':'组已经存在'}
        else:
            dictMerged=dict({'success':True,'msg':''},**self.data)
        return dictMerged


class HostForm(forms.Form):
    id = forms.IntegerField(label="ID",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': 'yes'}))
    c = models.Group.objects.all().values_list('id','name')
    group=forms.CharField(label="GroupSelect",widget=forms.Select(choices=c,attrs={'class':'form-control'}))
    systemtype=forms.CharField(label="SystemType",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),error_messages={'msg':'不可以为空'})
    manage_ip=forms.CharField(label="ManagerID",max_length=15,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    service_ip=forms.CharField(label="ServiceIP",max_length=15,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    outer_ip=forms.CharField(label="OuterIP",max_length=15,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    server_position=forms.CharField(label="ServerPos",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    hostname=forms.CharField(label="Hostname",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    normal_user=forms.CharField(label="NormalUser",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    sshpasswd=forms.CharField(label="Passwd",max_length=100,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    sshport=forms.CharField(label="Port",max_length=5,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    coreness=forms.IntegerField(label="Coreness",widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    memory=forms.IntegerField(label="Memory",widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    root_disk=forms.IntegerField(label="RootDisk",widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    share_disk=forms.IntegerField(label="ShareDisk",widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    share_disk_path=forms.CharField(label="ShareDiskPath",max_length=200,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    info=forms.CharField(label="Info",max_length=200,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))