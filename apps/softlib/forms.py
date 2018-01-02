# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
import models
from django.utils.translation import gettext_lazy as _

class SoftlibCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Softlib
        fields = ['soft_type','soft_version']
        widgets = {
            'soft_type': forms.Select(attrs={'type': 'select2 form-control'}),
        }
        labels = {
            'soft_type':'软件类型','soft_version':'软件版本'
        }