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
    return json.loads(response.decode('utf-8'))


def fetch_ECSPage():
    from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageNumber', 1)
    request.add_query_param('PageSize', 1)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['TotalCount']


def fetch_Instances(page):
    from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageNumber', page)
    request.add_query_param('PageSize', conf.ALIYUN_PAGESIZE)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['Instances']['Instance']


def fetch_RDSPage():
    from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageSize', 1)
    request.add_query_param('PageNumber', 1)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['TotalRecordCount']


def fetch_RDSs(page):
    from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageNumber', page)
    request.add_query_param('PageSize', conf.ALIYUN_PAGESIZE)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['Items']['DBInstance']
