# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime,json
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings

class AnalyzeCMSTool(AnalyzeTool):

    @staticmethod
    def change_timestamp(dataset):
        json_dataset = []
        for data in json.loads(dataset):
            d = datetime.datetime.fromtimestamp(data['timestamp'] / 1000)
            str1 = d.strftime("%Y/%m/%d %H:%M:%S")  # "%Y/%m/%d %H:%M:%S"
            data['timestamp'] = str1
            json_dataset.append(data)
        return json_dataset
