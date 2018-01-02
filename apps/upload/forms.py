# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from deveops.utils import aes,checkpass
class GroupUploadFileForm(forms.ModelForm):
    class Meta:
        model = models.GroupUpload
        fields = ['file']

    def before_save(self,request,commit):
        return request.POST.get('groups')

class StorageUploadFileForm(forms.ModelForm):
    class Meta:
        model = models.StorageUpload
        fields = ['file']

    def before_save(self,request,commit):
        pass



