# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
"""devEops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
import views
urlpatterns = [
    # VIEW
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^404/',views.ErrorView.as_view(),name='404'),
    # url(r'^permission/',views.PermissionView.as_view(),name='permission'),
    url(r'^validate/', include('validate.urls.views_urls', namespace='validate')),
    # url(r'^manager/', include('manager.urls.views_urls', namespace='manager')),
    # url(r'^operation/',include('operation.urls.views_urls',namespace='operation')),
    # url(r'^timeline/',include('timeline.urls.views_urls',namespace='timeline')),
    # url(r'^authority/',include('authority.urls.views_urls',namespace='authority')),
    # url(r'^application/',include('application.urls.views_urls',namespace='application')),
    # url(r'^concert/',include('concert.urls.views_urls',namespace='concert')),

    # API
    # url(r'^api-manager/', include('manager.urls.api_urls', namespace='api-manager')),
    # url(r'^api-operation/',include('operation.urls.api_urls',namespace='api-operation')),
    # url(r'^api-authority/',include('authority.urls.api_urls',namespace='api-authority')),
    # url(r'^api-application/',include('application.urls.api_urls',namespace='api-application')),
    # url(r'^api-concert/',include('concert.urls.api_urls',namespace='api-concert')),
]

'''
   
'''
