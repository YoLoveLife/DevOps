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