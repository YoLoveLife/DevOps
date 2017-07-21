# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class GroupForm(forms.Form):
    id=forms.IntegerField(label="ID",widget=forms.TextInput(attrs={'type':'text','class':'form-control','disabled':'yes'}))
    name=forms.CharField(label="Name",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    info=forms.CharField(label="Info",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))


class HostForm(forms.Form):
    name=forms.CharField(label="hostname",max_length=50)
    groupid=forms.IntegerField(label="groupid")
    sship=forms.CharField(label="sship",max_length=15)

    id = forms.IntegerField(label="ID",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'disabled': 'yes'}))
    # group = models.ForeignKey(Group,default=1,related_name='host_set')#所属应用
    group=GroupForm()
    systemtype=forms.CharField(label="Systemtype",max_length=50)
    manage_ip=forms.IntegerField(label="ManagerID")
    service_ip=forms.CharField(label="ServiceIP",max_length=15)
    outer_ip=forms.CharField(label="OuterIP",max_length=15)
    server_position=forms.CharField(label="ServerPos",max_length=50)
    hostname=forms.CharField(label="Hostname",max_length=50)
    normal_user=forms.CharField(label="NormalUser",max_length=50)
    sshpasswd=forms.CharField(label="Passwd",max_length=100)
    sshport=forms.CharField(label="Port",max_length=5)
    coreness=forms.IntegerField(label="Coreness")
    memory=forms.IntegerField(label="Memory")
    root_disk=forms.IntegerField(label="RootDisk")
    share_disk=forms.CharField(label="ShareDisk")
    share_disk_path=forms.CharField(label="ShareDiskPath",max_length=200)
    info=forms.CharField(label="Info",max_length=200)