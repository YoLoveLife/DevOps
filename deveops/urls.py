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
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # API
    path(r'api-auth/', include('authority.urls.api_urls')),
    path(r'api-manager/', include('manager.urls.api_urls')),
    path(r'api-ops/', include('ops.urls.api_urls')),
    path(r'api-utils/', include('utils.urls.api_urls')),
    path(r'api-work/', include('work.urls.api_urls')),
    path(r'api-var/', include('variable.urls.api_urls')),
    path(r'api-dns/', include('yodns.urls.api_urls')),
    path(r'api-cdn/', include('yocdn.urls.api_urls')),
    path(r'api-zdb/', include('zdb.urls.api_urls')),
    path(r'api-dashboard/', include('dashboard.urls.api_urls')),
    path(r'api-monitor/', include('monitor.urls.api_urls')),
    # path(r'api-console/', include('console.urls.api_urls')),
    path(r'api-ezsetup/', include('ezsetup.urls.api_urls')),
    path(r'api-ipool/', include('pool.urls.api_urls')),
    path(r'api-timeline/', include('timeline.urls.api_urls')),
    path(r'api-docs/', include_docs_urls(title=u'接口说明文档', authentication_classes=[], permission_classes=[])),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]




