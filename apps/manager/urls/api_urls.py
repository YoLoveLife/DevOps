# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from django.urls import path
from ..api import group as GroupAPI
from ..api import host as HostAPI

urlpatterns = [
    # Resource group api
    path(r'v1/group/', GroupAPI.ManagerGroupListAPI.as_view()),
    path(r'v1/group/bypage/', GroupAPI.ManagerGroupListByPageAPI.as_view()),
    path(r'v1/group/create/', GroupAPI.ManagerGroupCreateAPI.as_view()),
    path(r'v1/group/<uuid:pk>/detail/', GroupAPI.ManagerGroupDetailAPI.as_view()),
    path(r'v1/group/<uuid:pk>/update/', GroupAPI.ManagerGroupUpdateAPI.as_view()),
    path(r'v1/group/<uuid:pk>/delete/', GroupAPI.ManagerGroupDeleteAPI.as_view()),
    path(r'v1/group/<int:pk>/selecthost/', GroupAPI.ManagerGroupSelectHostAPI.as_view()),
    path(r'v1/group/byops/', GroupAPI.ManagerGroupListByOpsAPI.as_view()),
    #
    # Resource host api
    path(r'v1/host/',HostAPI.ManagerHostListAPI.as_view()),
    path(r'v1/host/bypage/', HostAPI.ManagerHostListByPageAPI.as_view()),
    path(r'v1/host/create/', HostAPI.ManagerHostCreateAPI.as_view()),
    path(r'v1/host/<uuid:pk>/update/', HostAPI.ManagerHostUpdateAPI.as_view()),
    path(r'v1/host/<uuid:pk>/selectgroup/', HostAPI.ManagerHostSelectGroupAPI.as_view()),
    path(r'v1/host/<uuid:pk>/delete/', HostAPI.ManagerHostDeleteAPI.as_view()),
    path(r'v1/host/<uuid:pk>/<int:qrcode>/passwd/', HostAPI.ManagerHostPasswordAPI.as_view()),
]