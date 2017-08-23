# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url

import apps.validate.views
from apps.validate.views import loginout as LoginoutViews

urlpatterns = [
    url(r'^login$', LoginoutViews.ValidateLoginView.as_view(), name='valudatelogin'),
    url(r'^logout$', LoginoutViews.ValidateLogoutView.as_view(), name='valudatelogout'),
    url(r'^dashboard/', apps.validate.views.ValidateDashBoardView.as_view(), name='valudatedashboard')
]
