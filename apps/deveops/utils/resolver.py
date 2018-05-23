# -*- coding:utf-8 -*-
# !/usr/bin/env python3
# Time 18-5-16
# Author Yo
# Email YoLoveLife@outlook.com


#解析阿里雲返回數據提供數據模型可接受的json數據
class AliyunECS2Json(object):
    @staticmethod
    def decode(data):
        dt = {}
        dt['status'] = data['Status']
        if data.__contains__('VpcAttributes'):
            if len(data['VpcAttributes']['PrivateIpAddress']['IpAddress'])!=0:
                dt['connect_ip'] = data['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]

        if data.__contains__('Tags'):
            tags_list = []
            for tag in data['Tags']['Tag']:
                tags_list.append(tag['TagKey'] + tag['TagValue'])
            dt['tags'] = ':'.join(tags_list)
        dt['recognition_id'] = data['InstanceId']
        dt['expired'] = data['ExpiredDay']
        dt['instancename'] = data['InstanceName']
        return dt


class AliyunRDS2Json(object):
    @staticmethod
    def decode(data):
        dt = {}
        dt['status'] = data['DBInstanceStatus']
        dt['recognition_id'] = data['DBInstanceId']
        dt['instancename'] = data['DBInstanceDescription']
        dt['expired'] = data['ExpiredDay']
        dt['version'] = data['EngineVersion']
        dt['readonly'] = len(data['ReadOnlyDBInstanceIds']['ReadOnlyDBInstanceId'])
        return dt



