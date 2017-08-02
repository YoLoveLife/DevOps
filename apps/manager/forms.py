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
        is_create_modify=self.data['id'];
        is_name_exist=models.Group.objects.filter(name=self.data['name']).exists()
        if is_name_exist and is_create_modify =='#New':
            return {'success':False,'msg':'组已经存在'}
        else:
            return {'success':True,'msg':'','data':self.data}


class HostForm(forms.ModelForm):
    class Meta:
        model = models.Host
        fields = ('id','group','storages','systemtype',
                 'manage_ip','service_ip','outer_ip',
                 'server_position','hostname','normal_user',
                 'sshpasswd','sshport','coreness','memory','root_disk','info')
    # id = forms.IntegerField(label="ID",
    #                         widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'yes'}))
    # c = models.Group.objects.all().values_list('id','name')
    # group=forms.CharField(label="GroupSelect",widget=forms.Select(choices=c,attrs={'class':'form-control'}))
    # storage=forms.CharField(label="Storage",max_length=100)
    # storagesss=forms.ModelMultipleChoiceField(label="Storagesss",widget=forms.CheckboxSelectMultiple,queryset=models.Storage.objects)
    # systemtype=forms.CharField(label="SystemType",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # manage_ip=forms.CharField(label="ManagerID",max_length=15,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # service_ip=forms.CharField(label="ServiceIP",max_length=15,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # outer_ip=forms.CharField(label="OuterIP",max_length=15,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # server_position=forms.CharField(label="ServerPos",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # hostname=forms.CharField(label="Hostname",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # normal_user=forms.CharField(label="NormalUser",max_length=50,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # sshpasswd=forms.CharField(label="Passwd",max_length=100,widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))
    # sshport=forms.CharField(label="Port",max_length=5,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # coreness=forms.CharField(label="Coreness",max_length=5,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # memory=forms.CharField(label="Memory",max_length=7,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # root_disk=forms.CharField(label="RootDisk",max_length=7,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    # info=forms.CharField(label="Info",max_length=200,widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))

    def is_valid(self):
        if self.data['manage_ip']!="" and self.data.has_key('group'):
            return True
        else:
            return False

    def clean(self):
        is_manageip_exist=models.Host.objects.filter(manage_ip=self.data['manage_ip']).exists()
        if is_manageip_exist and self.data['id']=='#New':
            return {'success':False,'msg':'该管理IP已经登记'}
        else:
            return {'success':True,'msg':'','data':self.data,}

class StorageForm(forms.Form):
    id = forms.IntegerField(label="ID",
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'readonly': 'yes'}))
    disk_size = forms.CharField(label="DiskSize", max_length=15,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    disk_path = forms.CharField(label="DiskPath", max_length=100,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    info = forms.CharField(label="Info", max_length=15,
                                widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))

    def is_valid(self):
        if self.data['disk_size']!="" and self.data['disk_path']!="" and self.data['info']!="":
            return True
        else:
            return False

    def clean(self):
        is_storage_exist = models.Storage.objects.filter(disk_path=self.data['disk_path']).exists()
        if is_storage_exist :
            return {'success':False,'msg':'该存储已经存在'}
        else:
            return {'success':True,'msg':'','data':self.data}