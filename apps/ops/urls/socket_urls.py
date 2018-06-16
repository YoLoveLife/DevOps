# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from ops import consumers
from django.conf.urls import url
ops_routing = [
    url(r'ansible/(?P<work>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/', consumers.MetaConsumer),
]