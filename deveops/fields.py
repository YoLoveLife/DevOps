# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-10-10
# Author Yo
# Email YoLoveLife@outlook.com
import json
from django.db import models
class JSONField(models.TextField):
    description = "Json"

    # :TODO Rebuild models Django1.8+ ADD
    def from_db_value(self, value, expression, connection, context):
        json_value = models.TextField.to_python(self, value)
        try:
            return json.loads(json_value)['value']
        except:
            pass

        return json_value

    def to_python(self, value):
        json_value = models.TextField.to_python(self, value)
        try:
            return json.loads(json_value)['value']
        except:
            pass

        return json_value

    def get_prep_value(self, value):
        return json.dumps({'value':value})



