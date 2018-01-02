# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes
from manager.models import Host
from deveops.utils import checkpass

class DBCreateUpdateForm(forms.ModelForm):
    service_ip = forms.CharField(required=True,max_length=15,label=u'业务IP')
    class Meta:
        model = models.DB
        fields = ['prefix','root_passwd',
                  'port','socket','datadir','service_ip']
        widgets = {
            'root_passwd': forms.TextInput(attrs={'type':'password'})
        }
        labels = {
            'prefix':'prefix','root_passwd':u'管理密码','port':u'服务端口',
            'socket':'Socket','datadir':u'数据目录',
        }

    def clean_service_ip(self):
        if Host.objects.filter(service_ip=self.cleaned_data['service_ip']).exists():
            pass
        else:
            raise forms.ValidationError(u'该主机不存在')
        service_ip = self.cleaned_data['service_ip']
        host = Host.objects.filter(service_ip=service_ip).get()
        self.instance.host = host
        return host

    def clean_root_passwd(self):
        root_passwd = self.cleaned_data['root_passwd']
        if checkpass.checkPassword(root_passwd):
            return aes.encrypt(root_passwd)
        else:
            raise forms.ValidationError(u'密码复杂度不足')

    def before_save(self,request):
        pass

class RedisCreateUpdateForm(forms.ModelForm):
    service_ip = forms.CharField(required=True,max_length=13,label=u'业务IP')
    logfile = forms.CharField(required=False,max_length=100,label=u'日志文件')
    class Meta:
        model = models.Redis
        fields = ['prefix','redis_passwd','port','pidfile','logfile','service_ip']
        widgets = {
            'redis_passwd': forms.TextInput(attrs={'type':'password'})
        }
        labels = {
            'prefix':'prefix','redis_passwd':u'访问密码',u'port':'服务端口',
            'pidfile':u'进程文件'
        }

    def clean_redis_passwd(self):
        redis_passwd = self.cleaned_data['redis_passwd']
        if checkpass.checkPassword(redis_passwd):
            self.instance.root_passwd = aes.encrypt(redis_passwd)
            return aes.encrypt(redis_passwd)
        else:
            raise forms.ValidationError(u'密码复杂度不足')

    def clean_service_ip(self):
        if Host.objects.filter(service_ip=self.cleaned_data['service_ip']).exists():
            pass
        else:
            raise forms.ValidationError(u'该主机不存在')
        service_ip = self.cleaned_data['service_ip']
        host = Host.objects.filter(service_ip=service_ip).get()
        self.instance.host = host
        return host