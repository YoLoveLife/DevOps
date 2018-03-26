# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-23
# Author Yo
# Email YoLoveLife@outlook.com

from aliyunsdkcore import client
import json
AccessKeyId='LTAI7ypdSL872FxD'
AccessKeySecret='3f8MjiAxn3JbsuTuy43JR6o0ayPd82'
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')

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

# if __name__ == '__main__':
#     fetch_Instance('i-bp1c3euzhnq4pbi6j3xs')