# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from django.urls import path
from console.api import truck as TruckAPI
urlpatterns=[
    # Resource console api
    path(r'v1/truck/create/', TruckAPI.ConsoleTruckCreateAPI.as_view()),
]