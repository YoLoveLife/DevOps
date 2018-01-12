# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from .. import views
urlpatterns = [
    #Resource group url
    url(r'^group/$', views.UploadGroupFile.as_view(), name='groupupload'),
    url(r'^group-framework/$', views.UploadFrameworkGroupFile.as_view(),name='groupframeworkupload'),
    url(r'^storage/$',views.UploadStorageFile.as_view(),name='storageload'),
]