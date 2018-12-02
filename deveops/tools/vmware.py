# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-26
# Author Yo
# Email YoLoveLife@outlook.com
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
# django.setup()
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from django.conf import settings as DJANGO_SETTINGS


class VmwareTool(object):
    def __init__(self, VMWARE_SERVER, VMWARE_USERNAME, VMWARE_PASSWD):
        self.server = VMWARE_SERVER
        self.service_instance = connect.SmartConnectNoSSL(
            host=VMWARE_SERVER,
            user=VMWARE_USERNAME,
            pwd=VMWARE_PASSWD,
            port=443
        )

        atexit.register(connect.Disconnect, self.service_instance)

    def get_all_vms(self):
        try:
            content = self.service_instance.RetrieveContent()
            container = content.rootFolder
            viewType = [vim.VirtualMachine]
            recursive = True
            containerView = content.viewManager.CreateContainerView(
                container, viewType, recursive
            )
            children = containerView.view
            return children
        except vmodl.MethodFault as error:
            return -1

    @staticmethod
    def get_vm_status(info):
        if info != 'poweredOn':
            return DJANGO_SETTINGS.STATUS_HOST_CLOSE
        else:
            return DJANGO_SETTINGS.STATUS_HOST_CAN_BE_USE

    @staticmethod
    def get_vm_models(vm, server):
        '''
        :param vm: VMware API 返回的vm對象
        :return: 返回一個可以直接被models存儲的字典對象
        '''
        return {
            'hostname': vm.config.name,
            'connect_ip': vm.summary.guest.ipAddress or '127.0.0.1',
            'sshport': 52000,
            'status': VmwareTool.get_vm_status(vm.summary.runtime.powerState),
            'systemtype': vm.config.guestFullName,
            'position': 'Center{IP}'.format(IP=server),
            'vmware_id': vm.config.uuid,
        }

    @staticmethod
    def get_vm_detail(vm):
        '''
        :param vm: VMware API 返回的vm對象
        :return: 返回該主機所有信息字典
        '''
        return {
            'extend': {
                'memory': vm.config.hardware.memoryMB,
                'cpus': vm.config.hardware.numCPU,
            }
        }

    def get_vm_monitor(self,vm):
        try:
            content = self.service_instance.RetrieveContent()
            perfManager = content.perfManager
            metricId = vim.PerformanceManager.MetricId(counterId=2, instance="*")
            import datetime
            startTime = datetime.datetime.now() - datetime.timedelta(hours=3)
            endTime = datetime.datetime.now()
            # query = vim.PerformanceManager.QuerySpec(maxSample=1,
            #                                          entity=vm,
            #                                          metricId=[metricId],
            #                                          startTime=startTime,
            #                                          endTime=endTime)
            # query = vim.PerformanceManager.QueryAvailablePerfMetric(entity=vm,
            #                                                         startTime=startTime,
            #                                                         endTime=endTime)
            query = perfManager.QueryPerfProviderSummary(entity=vm)
            print(query)
            # print(perfManager.QueryPerf(querySpec=[query]))
            # print(perfManager.QueryPerfCounter(counterId=[24,]))
            # print(perfManager.QueryPerfCounterByLevel(level=1))
            '''
                2 CPU 在该时间间隔内的使用情况(百分比) CPU
                24 内存使用情况，表示为占总的配置或可用内存的百分比 MEMORY
                136 收集时间间隔内每秒钟磁盘平均读取次数 DISK OUT
                137 收集时间间隔内每秒钟磁盘平均写入次数 DISK IN
                146 该时间间隔内收到的数据包数 NETWORK
            '''
        except vmodl.MethodFault as e:
            print("Caught vmodl fault : " + e.msg)
            return -1
        except Exception as e:
            print("Caught exception : " + str(e))
        return -1