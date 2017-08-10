# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
from django.contrib.auth.forms import AuthenticationForm
class LoginForm(forms.Form):
    email=forms.EmailField(label="Username",max_length=100,widget=forms.TextInput(attrs={'type':'email','class':'form-control','placeholder':'Email'}))
    passwd=forms.CharField(label="Passwd",widget=forms.PasswordInput(attrs={'type':'password','class':'form-control','placeholder':'Password'}))