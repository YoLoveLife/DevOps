# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes
from manager.models import Host
# 验证器
def service_ip_validator(value):
    try:
        host = Host.objects.filter(service_ip=value).get()
    except Exception as e:
        raise forms.ValidationError(u'该主机不存在')

class DBCreateUpdateForm(forms.ModelForm):
    service_ip = forms.CharField(required=True,max_length=15,label='业务IP',validators=[service_ip_validator])
    class Meta:
        model = models.DB
        fields = ['prefix','root_passwd',
                  'port','socket','datadir','service_ip']
        widgets = {
            'root_passwd': forms.TextInput(attrs={'type':'password'})
        }
        labels = {
            'prefix':'prefix','root_passwd':'管理密码','port':'服务端口',
            'socket':'Socket','datadir':'数据目录',
        }

    def clean_service_ip(self):
        service_ip = self.cleaned_data['service_ip']
        host = Host.objects.filter(service_ip=service_ip).get()
        self.instance.host = host
        return host

    def clean_root_passwd(self):
        root_passwd = self.cleaned_data['root_passwd']
        self.instance.root_passwd = aes.encrypt(root_passwd)
        return aes.encrypt(root_passwd)

    # def before_save(self,request,commit):
    #     service_ip = request.POST.get('service_ip')
    #     if Host.objects.filter(service_ip = service_ip).count() == 1:
    #         host = Host.objects.filter(service_ip=service_ip).get()
    #         self.instance.host = host
    #     else:
    #         pass
    #     return self.save(commit=commit)

class RedisCreateUpdateForm(forms.ModelForm):
    service_ip = forms.CharField(required=True,max_length=13,label='业务IP')
    logfile = forms.CharField(required=False,max_length=100,label='日志文件')
    class Meta:
        model = models.Redis
        fields = ['prefix','redis_passwd','port','pidfile','logfile','service_ip']
        widgets = {
            'redis_passwd': forms.TextInput(attrs={'type':'password'})
        }
        labels = {
            'prefix':'prefix','redis_passwd':'访问密码','port':'服务端口',
            'pidfile':'进程文件'
        }

