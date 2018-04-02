# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-26
# Author Yo
# Email YoLoveLife@outlook.com

Config_Key={
    'memorySizeMB': '内存大小',
    'numCpu': 'CPU个数',
    'name': '名称',
    'uuid': 'UUID',
    'guestFullName': '操作系统'
}
RunTime_Key={
    # 'bootTime':'重启时间',
    'powerState': '电源状态',
}
Guest_Key={
    'ipAddress':'IP地址',
}
Hardware_Key={
    'memoryMB':'内存大小',
}
QuickStats_Key={
    'overallCpuUsage': '消耗主机CPU MHz',
    'guestMemoryUsage':'活动客户机内存',
    'hostMemoryUsage':'已消耗主机内存',
    'privateMemory': '专用内存',
    'sharedMemory': '共享内存',
    'uptimeSeconds': '启动时长',
}
Storage_Key={
    'committed':'置备存储',
    'unshared':'未共享存储'
}
from pyVim import connect
import ssl
from deveops import conf as DEVEOPS_CONF
USERNAME = DEVEOPS_CONF.VMWARE_USERNAME
PASSWORD = DEVEOPS_CONF.VMWARE_PASSWD
SERVER = DEVEOPS_CONF.VMWARE_SERVER

ssl._create_default_https_context = ssl._create_unverified_context


def VMconnect(SERVER):
    my_cluster = connect.Connect(SERVER,443,USERNAME,PASSWORD)
    return my_cluster


def VMsearch(UUID,my_cluster):
    searcher = my_cluster.content.searchIndex
    vm = searcher.FindByUuid(uuid=UUID,vmSearch=True)
    return vm


def to_list(obj,keys):
    list= {}
    for key in keys:
        list[key] = getattr(obj, key, 'null')
    return list


def FetchConfig(vm):
    obj = vm.summary.config
    return to_list(obj,Config_Key.keys())


def FetchRunTime(vm):
    obj = vm.summary.runtime
    return to_list(obj, RunTime_Key.keys())


def FetchGuest(vm):
    obj = vm.summary.guest
    return to_list(obj, Guest_Key.keys())


def FetchQuickStats(vm):
    obj = vm.summary.quickStats
    return to_list(obj, QuickStats_Key.keys())


def FetchStorage(vm):
    obj = vm.summary.storage
    return to_list(obj, Storage_Key.keys())


def FetchHardware(vm):
    obj = vm.config.hardware
    return to_list(obj, Hardware_Key.keys())


def FetchInfo(vm):
    list = {}
    list = dict(FetchConfig(vm),**FetchRunTime(vm))
    list = dict(list,**FetchGuest(vm))
    list = dict(list,**FetchQuickStats(vm))
    list = dict(list,**FetchStorage(vm))
    list = dict(list,**FetchHardware(vm))
    return list


def VMdisconnect(my_cluter):
    connect.Disconnect(my_cluter)

def fetch_Instance(uuid):
    cluster = VMconnect(SERVER)
    vm = VMsearch(uuid,cluster)
    if vm is None:
        list = {}
    else:
        list = FetchInfo(vm)

    VMdisconnect(cluster)
    return list


def fetch_AllInstance():
    cluster = VMconnect(SERVER)
    content = cluster.RetrieveContent()
    container = content.rootFolder
    from pyVmomi import vim

    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
    children = containerView.view
    return children

if __name__ == "__main__":
    cluster = VMconnect(SERVER)
    vm = VMsearch("123",cluster)
    print(vm.name)
    # print(FetchInfo(vm))
    VMdisconnect(cluster)
