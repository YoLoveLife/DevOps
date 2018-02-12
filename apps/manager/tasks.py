# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from celery import shared_task
@shared_task
def update_host_info(host):
    task_tuple=(
        ('setup','')
    )

