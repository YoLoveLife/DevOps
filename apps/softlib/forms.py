# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _

class StorageCreateUpdateForm(forms.ModelForm):
    #
    class Meta:
        model = models.Softlib
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