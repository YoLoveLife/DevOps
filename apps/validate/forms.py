# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'账户'}))
    passwd = forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'type':'password','class':'form-control','placeholder':'密码'}))
    verify = forms.CharField(label="验证码",max_length=4,widget=forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'验证码'}))