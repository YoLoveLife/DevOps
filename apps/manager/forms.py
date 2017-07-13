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
    remark=forms.CharField(label="Remark",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))


class HostForm(forms.Form):
    name=forms.CharField(label="hostname",max_length=50)
    groupid=forms.IntegerField(label="groupid")
    sship=forms.CharField(label="sship",max_length=15)
