# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from ..views import UtilsManageView
urlpatterns = [
    #Resource dashboard url
    url(r'^$', UtilsManageView.as_view(),name='manage')
]