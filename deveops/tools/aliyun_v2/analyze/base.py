# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import json


class AnalyzeTool(object):
    @staticmethod
    def results_to_json(result):
        return json.loads(result.decode('utf-8'))

    @staticmethod
    def get_expired_day(time):
        pass

    @staticmethod
    def get_models(result):
        pass

    @staticmethod
    def get_expired_models(result):
        pass