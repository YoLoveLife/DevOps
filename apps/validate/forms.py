# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 03 17:37
# Author Yo
# Email YoLoveLife@outlook.com
from django import forms
from django.contrib.auth.models import User   # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm
from models import ExtendUser
from django.contrib.auth import get_user_model
class LoginForm(forms.Form):
    username=forms.CharField(label="用户名",max_length=100,widget=forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'账户'}))
    passwd=forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'type':'password','class':'form-control','placeholder':'密码'}))