# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-5-30
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf import settings
enable_utc = False
timezone = 'Asia/Shanghai'
broker_url = "redis://:{PASSWORD}@{HOST}:{PORT}/{SPACE}".format(
    PASSWORD=settings.REDIS_PASSWD,
    HOST=settings.REDIS_HOST,
    PORT=settings.REDIS_PORT,
    SPACE=settings.REDIS_SPACE
)
task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = ['json', 'pickle',]
# worker_log_format = '%(message)s'
# worker_task_log_format = '%(message)s'
# task_eager_propagates = True
# worker_redirect_stdouts = True
# worker_redirect_stdouts_level = "INFO"
# worker_hijack_root_logger = False