# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-28
# Author Yo
# Email YoLoveLife@outlook.com
import xlrd
from upload.models import GroupUpload
from manager.models import Host,Group
from deveops.utils import aes
from django.db.models.query import QuerySet
def ToDictFromExcel(rowdata):
    service_ip = 0
    server_position = 1
    normal_user = 2
    sshport = 3
    sshpasswd = 4
    info = 5
    manage_ip = 7
    outer_ip = 7
    hostname = 8
    systemtype = 9
    if Host.objects.filter(service_ip=rowdata[service_ip].value).exists():
        return {}
    else:
        return {
            'service_ip':rowdata[service_ip].value,'server_position':rowdata[server_position].value,
            'normal_user':rowdata[normal_user].value,'sshpasswd':aes.encrypt(rowdata[sshpasswd].value),
            'sshport':int(rowdata[sshport].value),'info':rowdata[info].value,
            'manage_ip':rowdata[manage_ip].value,'outer_ip':rowdata[outer_ip].value,
            'hostname':rowdata[hostname].value,'systemtype':rowdata[systemtype].value,
            }

def AnalyzeHostFromExcel(group_id,filename):
    group = Group.objects.get(id=group_id)
    upload = GroupUpload.objects.filter(file='%s'%(filename)).get()
    workbook = xlrd.open_workbook(upload.get_full_path())
    table = workbook.sheets()[0]
    for i in range(table.nrows)[3:]:
        dict = ToDictFromExcel(table.row(i))
        if dict:
            host = Host(**dict)
            host.save()
            host.groups.clear()
            host.groups.add(group)
            host.save()
        else:
            pass

if __name__ == '__main__':
    AnalyzeHostFromExcel(1,'xmt.xls')

