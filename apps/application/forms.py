# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes
from manager.models import Host
class DBCreateUpdateForm(forms.ModelForm):
    service_ip = forms.CharField(required=True,max_length=15,label='业务IP')
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
        error_messages={
            'service_ip':'ddr'
        }
    def clean(self):
        try:
            service_ip = self.cleaned_data['service_ip']
            host = Host.objects.filter(service_ip=service_ip).get()
            self.cleaned_data.update({'service_ip':host})
        except Exception as e:
            raise forms.ValidationError(u'该主机不存在')
        return super(DBCreateUpdateForm,self).clean()

    def before_save(self,request,commit):
        service_ip = request.POST.get('service_ip')
        self.instance.root_passwd = aes.encrypt(self.instance.root_passwd)
        if Host.objects.filter(service_ip = service_ip).count() == 1:
            host = Host.objects.filter(service_ip=service_ip).get()
            self.instance.host = host
        else:
            pass
        return self.save(commit=commit)

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

