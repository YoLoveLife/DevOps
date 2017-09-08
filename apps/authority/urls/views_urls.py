# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from ..views import group as GroupView
urlpatterns = [
    # url(r'^dashboard/', views.AuthorityDashboardViewView.as_view(), name='authoritydashboard'),
    url(r'^group/', GroupView.AuthorityGroupView.as_view(), name='authoritygroup'),
    # url(r'^user/', views.AuthorityUserView.as_view(), name='authorityuser'),
    # url(r'^permission/', views.AuthorityPermissionView.as_view(),name='authoritypermission'),
]
