# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
from django.conf import settings
from qingcloud import iaas


class QingCloudTool(object):
    def __init__(self):
        self.clt = iaas.connect_to_zone(
            'pek1',
            settings.QINGCLOUD_ACCESSKEY,
            settings.QINGCLOUD_ACCESSSECRET,
        )

    def init_action(self):
        pass

