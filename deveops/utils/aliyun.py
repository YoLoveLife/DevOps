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


def fetch_KVStorePage():
    from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest

    # 设置参数
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageSize', 1)
    request.add_query_param('PageNumber', 1)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['TotalCount']


def fetch_KVStores(page):
    from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest

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
    return data['Instances']['KVStoreInstance']


def fetch_MongoDBPage():
    from aliyunsdkdds.request.v20151201 import DescribeDBInstancesRequest

    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageSize', 30)
    request.add_query_param('PageNumber', 1)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['TotalCount']


def fetch_MongoDBs(page):
    from aliyunsdkdds.request.v20151201 import DescribeDBInstancesRequest

    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_accept_format('json')

    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PageNumber', page)
    request.add_query_param('PageSize', 30)

    try:
        response = clt.do_action_with_exception(request)
    except:
        return {}
    data = json.loads(response.decode('utf-8'))
    return data['DBInstances']['DBInstance']


def ddr():
    from aliyunsdkcore import client
    from aliyunsdkcms.request.v20180308 import QueryMetricListRequest

    request = QueryMetricListRequest.QueryMetricListRequest()
    request.set_accept_format('json')

    request.add_query_param('Project', 'acs_ecs_dashboard')
    request.add_query_param('Metric', 'CPUUtilization')
    request.add_query_param('StartTime', '2018-5-25 00:00:00')
    request.add_query_param('EndTime', '2018-6-1 12:01:01')
    request.add_query_param('Period', '900')
    request.add_query_param('Dimensions', {"instanceId":"i-bp19rye0fhrc4k01ztsz"})

    # 发起请求
    response = clt.do_action_with_exception(request)
    data = json.loads(response.decode('utf-8'))
    newjson = json.loads(data['Datapoints'])
    import time
    x = []
    for d in newjson:
        time_local = time.localtime(d['timestamp'])
        x.append(time.strftime("%m-%d %H:%M", time_local))
    print(x)


if __name__ == '__main__':
    ddr()


