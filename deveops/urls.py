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
# from django.conf.urls import url
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    # API
    path(r'api-auth/', include('authority.urls.api_urls')),
    path(r'api-manager/', include('manager.urls.api_urls')),
    path(r'api-ops/', include('ops.urls.api_urls')),
    path(r'api-utils/', include('utils.urls.api_urls')),
    path(r'api-work/', include('work.urls.api_urls')),
    path(r'api-var/', include('variable.urls.api_urls')),
    path(r'api-dns/', include('dns.urls.api_urls')),
    # path(r'api-app/', include('application.urls.api_urls')),
    # url(r'^api-application/',include('application.urls.api_urls',namespace='api-application')),
    # url(r'^api-execute/',include('execute.urls.api_urls',namespace='api-execute')),
    # url(r'^api-softlib/',include('softlib.urls.api_urls',namespace='api-softlib')),
    path(r'api-utils/', include('utils.urls.api_urls')),
    path(r'api-dashboard/', include('dashboard.urls.api_urls')),

    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]

'''
   
'''
