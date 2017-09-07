# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from ..views import loginout as LoginoutViews
from ..views import dashboard as DashboardViews
from ..views import user as UserViews
urlpatterns = [
    url(r'^login$', LoginoutViews.ValidateLoginView.as_view(), name='valudatelogin'),
    url(r'^logout$', LoginoutViews.ValidateLogoutView.as_view(), name='valudatelogout'),
    url(r'^dashboard/', DashboardViews.ValidateDashboardView.as_view(), name='validatedashboard'),
    url(r'^user/', UserViews.ValidateUserListView.as_view(),name='validateuser'),
]
