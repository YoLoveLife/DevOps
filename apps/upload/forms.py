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
        fields = ['file','group']
        labels = {
            'group':u'应用组'
        }
        widgets = {
            'group':forms.Select(attrs={'type': 'select2 form-control'}),
        }
    def clean_group(self):
        group = self.cleaned_data['group']
        return group
    def clean_file(self):
        file = self.cleaned_data['file']
        str_file = file.name.encode('unicode-escape').decode('string_escape')
        if str_file.count('.') > 1:
            raise forms.ValidationError(u'您上传了恶意的信息 已经记录了您的操作信息')
        if not (str_file.endswith('.xls') or str_file.endswith('.xlsx')):
            raise forms.ValidationError(u'您的文件可能包含恶意内容 已经记录了您的操作信息')
        return file

class GroupFrameworkUploadFileForm(forms.ModelForm):
    class Meta:
        model = models.GroupFrameworkUpload
        fields = ['file','group']
        labels = {
            'group':u'应用组'
        }
        widgets = {
            'group':forms.Select(attrs={'type': 'select2 form-control'}),
        }
    def clean_group(self):
        group = self.cleaned_data['group']
        return group

    def clean_file(self):
        file = self.cleaned_data['file']
        str_file = file.name.encode('unicode-escape').decode('string_escape')
        if str_file.count('.') > 1:
            raise forms.ValidationError(u'您上传了恶意的信息 已经记录了您的操作信息')
        if not (str_file.endswith('.jpg') or str_file.endswith('.png') or str_file.endswith('.jpeg')):
            raise forms.ValidationError(u'您的文件可能包含恶意内容 已经记录了您的操作信息')
        return file


class StorageUploadFileForm(forms.ModelForm):
    class Meta:
        model = models.StorageUpload
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        str_file = file.name.encode('unicode-escape').decode('string_escape')
        if str_file.count('.') > 1:
            raise forms.ValidationError(u'您上传了恶意的信息 已经记录了您的操作信息')
        if not (str_file.endswith('.xls') or str_file.endswith('.xlsx')):
            raise forms.ValidationError(u'您的文件可能包含恶意内容 已经记录了您的操作信息')
        return file



