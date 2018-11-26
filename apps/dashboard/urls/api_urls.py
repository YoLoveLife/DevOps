# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from django.urls import path
from ..api import dashboard as DashboardAPI
urlpatterns = [
    # Resource dashboard api
    path(r'v1/count/', DashboardAPI.DashboardCountAPI.as_view()),
    path(r'v1/work/', DashboardAPI.DashboardWorkAPI.as_view()),
    path(r'v1/group/', DashboardAPI.DashboardGroupAPI.as_view()),
]
