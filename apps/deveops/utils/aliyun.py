# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-23
# Author Yo
# Email YoLoveLife@outlook.com

from aliyunsdkcore import client
import json
from deveops import conf
clt = client.AcsClient(conf.ALIYUN_ACCESSKEY, conf.ALIYUN_ACCESSSECRET, 'cn-hangzhou')

def fetch_Instance(instance):
    from aliyunsdkecs.request.v20140526 import DescribeInstanceAttributeRequest
    request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
    request.set_accept_format('json')
    request.add_query_param('InstanceId',instance)
    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    return json.loads(response)