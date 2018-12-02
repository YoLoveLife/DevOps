# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from django.urls import path
from ..api import user
from ..api import group
from ..api import permission
from ..api import key
from ..api import jumper

urlpatterns = [
    # Resource login api
    path(r'login/', user.UserLoginAPI.as_view()),
    path(r'userinfo/', user.UserInfoAPI.as_view()),
    #
    # Resource user api
    path(r'v1/user/', user.UserListAPI.as_view()),
    path(r'v1/user/bypage/', user.UserListByPageAPI.as_view()),
    path(r'v1/opsuser/', user.UserOpsListAPI.as_view()),
    path(r'v1/opsuser/bypage/', user.UserOpsListByPageAPI.as_view()),
    path(r'v1/user/create/', user.UserCreateAPI.as_view()),
    path(r'v1/user/<int:pk>/update/', user.UserUpdateAPI.as_view()),
    path(r'v1/user/<int:pk>/delete/', user.UserDeleteAPI.as_view()),
    path(r'v1/user/qrcode/', user.UserQRCodeAPI.as_view()),
    path(r'v1/user/expire/', user.UserExpireAPI.as_view()),
    #
    # Resource group api
    path(r'v1/group/', group.GroupListAPI.as_view()),
    path(r'v1/group/bypage/', group.GroupListByPageAPI.as_view()),
    path(r'v1/group/create/', group.GroupCreateAPI.as_view()),
    path(r'v1/group/<int:pk>/update/', group.GroupUpdateAPI.as_view()),
    path(r'v1/group/<int:pk>/delete/', group.GroupDeleteAPI.as_view()),
    #
    # Resource key api
    path(r'v1/key/', key.KeyListAPI.as_view()),
    path(r'v1/key/bypage/', key.KeyListByPageAPI.as_view()),
    path(r'v1/key/create/', key.KeyCreateAPI.as_view()),
    path(r'v1/key/<uuid:pk>/update/', key.KeyUpdateAPI.as_view()),
    path(r'v1/key/<uuid:pk>/delete/', key.KeyDeleteAPI.as_view()),
    #
    # Resource jumper api
    path(r'v1/jumper/', jumper.JumperListAPI.as_view()),
    path(r'v1/jumper/bypage/', jumper.JumperListByPageAPI.as_view()),
    path(r'v1/jumper/<uuid:pk>/status/', jumper.JumperStatusAPI.as_view()),
    path(r'v1/jumper/create/', jumper.JumperCreateAPI.as_view()),
    path(r'v1/jumper/<uuid:pk>/update/', jumper.JumperUpdateAPI.as_view()),
    path(r'v1/jumper/<uuid:pk>/delete/', jumper.JumperDeleteAPI.as_view()),
    #
    # Resource permission api
    path(r'v1/permission/',permission.PermissionListAPI.as_view()),
]
