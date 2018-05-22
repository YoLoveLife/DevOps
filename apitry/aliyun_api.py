# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-26
# Author Yo
# Email YoLoveLife@outlook.com
import xlrd
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import CreateLoadBalancerHTTPListenerRequest,CreateLoadBalancerHTTPSListenerRequest,DeleteLoadBalancerListenerRequest,DescribeLoadBalancerHTTPListenerAttributeRequest,DescribeLoadBalancerHTTPSListenerAttributeRequest,StartLoadBalancerListenerRequest
from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest
import aliyun_api_conf as ALICONF
class AliYun_SLB_API(object):
    def __init__(self):
        self.clt = client.AcsClient(ALICONF.accessKeyId,ALICONF.accessSecret,'cn-hangzhou')
        self.request = None

    def StartHttpListener(self,**kwargs):
        self.request = None
        self.request = StartLoadBalancerListenerRequest.StartLoadBalancerListenerRequest()
        self.request.set_accept_format('json')

        self.request.add_query_param('LoadBalancerId', kwargs['LoadBalancerId'])
        self.request.add_query_param('ListenerPort', kwargs['ListenerPort'])


    def CreateHttpListener(self,**kwargs):
        self.request = None
        if kwargs['https']==0:
            self.request = CreateLoadBalancerHTTPListenerRequest.CreateLoadBalancerHTTPListenerRequest()
        else:
            self.request = CreateLoadBalancerHTTPSListenerRequest.CreateLoadBalancerHTTPSListenerRequest()
            self.request.add_query_param('ServerCertificateId', kwargs['ServerCertificateId'])
        self.request.set_accept_format('json')
        self.request.add_query_param('LoadBalancerId', kwargs['LoadBalancerId'])
        self.request.add_query_param('Bandwidth', kwargs['Bandwidth'])
        self.request.add_query_param('ListenerPort', kwargs['ListenerPort'])
        self.request.add_query_param('StickySession', kwargs['StickySession'])
        self.request.add_query_param('HealthCheck', kwargs['HealthCheck'])
        self.request.add_query_param('BackendServerPort', kwargs['BackendServerPort'])
        self.request.add_query_param('XForwardedFor', kwargs['XForwardedFor'])
        self.request.add_query_param('Scheduler', kwargs['Scheduler'])
        self.request.add_query_param('StickySessionType', kwargs['StickySessionType'])
        self.request.add_query_param('CookieTimeout', kwargs['CookieTimeout'])
        self.request.add_query_param('HealthCheckDomain', kwargs['HealthCheckDomain'])
        self.request.add_query_param('HealthCheckURI', kwargs['HealthCheckURI'])
        self.request.add_query_param('HealthyThreshold', kwargs['HealthyThreshold'])
        self.request.add_query_param('UnhealthyThreshold', kwargs['UnhealthyThreshold'])
        self.request.add_query_param('HealthCheckInterval', kwargs['HealthCheckInterval'])
        self.request.add_query_param('HealthCheckTimeout',kwargs['HealthCheckTimeout'])

    def DeleteListener(self,**kwargs):
        self.request = None
        self.request = DeleteLoadBalancerListenerRequest.DeleteLoadBalancerListenerRequest()
        self.request.set_accept_format('json')

        self.request.add_query_param('LoadBalancerId', kwargs['LoadBalancerId'])
        self.request.add_query_param('ListenerPort', kwargs['ListenerPort'])

    def DescribeHealthStatus(self,**kwargs):
        self.request = None
        self.request =DescribeHealthStatusRequest.DescribeHealthStatusRequest()
        self.request.add_query_param('LoadBalancerId', kwargs['LoadBalancerId'])

    def DescribeListener(self,**kwargs):
        self.request = None
        if kwargs['https']==0:
            self.request = DescribeLoadBalancerHTTPListenerAttributeRequest.DescribeLoadBalancerHTTPListenerAttributeRequest()
        else:
            self.request = DescribeLoadBalancerHTTPSListenerAttributeRequest.DescribeLoadBalancerHTTPSListenerAttributeRequest()

        self.request.add_query_param('LoadBalancerId', kwargs['LoadBalancerId'])
        self.request.add_query_param('ListenerPort', kwargs['ListenerPort'])
        self.request.set_accept_format('json')

    def send(self):
        response = self.clt.do_action_with_exception(self.request)
        print(response)
        return response

def solve_rowdata(rowdata):
    return {
        'LoadBalancerId':rowdata[1].value,
        'https':int(rowdata[2].value),
        'Bandwidth':int(rowdata[3].value),
        'ListenerPort':int(rowdata[4].value),
        'StickySession':rowdata[5].value,
        'HealthCheck':rowdata[6].value,
        'BackendServerPort':int(rowdata[7].value),
        'XForwardedFor':rowdata[8].value,
        'Scheduler':rowdata[9].value,
        'StickySessionType':rowdata[10].value,
        'CookieTimeout':int(rowdata[11].value),
        'HealthCheckDomain':rowdata[12].value,
        'HealthCheckURI':rowdata[13].value,
        'HealthyThreshold':int(rowdata[14].value),
        'UnhealthyThreshold':int(rowdata[15].value),
        'HealthCheckInterval':int(rowdata[16].value),
        'HealthCheckTimeout':int(rowdata[17].value),
        'ServerCertificateId':rowdata[18].value,
        }


def catch_rowdata(kk):
    workbook = xlrd.open_workbook('./listener2.xls')
    table = workbook.sheets()[0]
    for i in range(table.nrows)[1:]:
        dit = solve_rowdata(table.row(i))
        # kk.DescribeHealthStatus(**dit)
        # kk.DeleteListener(**dit)

        kk.CreateHttpListener(**dit)
        kk.send()
        kk.StartHttpListener(**dit)
        kk.send()

        # kk.StartHttpListener(**dit)
        # kk.send()

if __name__ == '__main__':
    kk = AliYun_SLB_API()
    catch_rowdata(kk)