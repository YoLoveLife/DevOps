# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17 20:16
# Author Yo
# Email YoLoveLife@outlook.com
from login.models import User
def permitlogin(username,userpasswd):
    user=User.objects.get(email=username)
    if user.password==userpasswd:
        return 1
    else:
        return 0