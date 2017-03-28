# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17 17:18
# Author Yo
# Email YoLoveLife@outlook.com
from models import Group
from django.core import serializers
from util import toJSON,str2dict
from anweb.models import Group,Host,Softlib,Soft
from django.forms.models import model_to_dict
from event import allevent
from inventory import maker
import json

'''
PARM:null
RETURN:list
USE:返回所有组的列表
'''
def group9groupsearch():
    a = Group.objects.all()
    list = []
    for i in a:
        list.append(toJSON(i))
    return list

'''
PARM:group_id,group_name,group_remark
RETURN:TRUE/FALSE
USE:如果组不存在 则添加组；如果组存在 则修改组
'''
def group9modifygroup(group_id,group_name,group_remark):
    if group_id == "0":#ADD
        group=Group(group_name=unicode.encode(group_name),remark=unicode.encode(group_remark))
        group.save()
    else:#UPDATE
        Group.objects.filter(id=int(group_id)).update(group_name=unicode.encode(group_name),remark=unicode.encode(group_remark))

'''
PARM:group_id
RETURN:返回组相关的信息
USE:
'''
def host9hostsearch(group_id):
    hostlist = Host.objects.filter(group_id=int(group_id))#需要展示的用户列表
    #需要从用户列表中 添加app-type的数据
    type_list=Soft.objects.all()
    list=[]
    for host in hostlist:
        tmpdict=model_to_dict(host)
        tmpdict['app_type']=host.softlib.soft_type.soft_name
        list.append(json.dumps(tmpdict))
    return list

'''
PARM:appname
RETURN:返回应用程序的版本
USE:
'''
def batch9appversion(appname):
    soft=Soft.objects.filter(soft_name=appname)
    versionlist=Softlib.objects.filter(soft_type=soft)
    list=[]
    for version in versionlist:
        tmpdict=model_to_dict(version)
        list.append(json.dumps(tmpdict))
    return list

'''
PARM:info for install tomcat
RETURN:执行结果
USE:
'''
def batch9tomcatinstall(iplist,javaversion,javaprefix,tomcatversion,tomcatprefix):
    tomcatlib=Softlib.objects.get(id=tomcatversion)
    javalib=Softlib.objects.get(id=javaversion)

    tomcatversion =tomcatlib.soft_version
    javaversion=javalib.soft_version
    javacheck=javalib.soft_md5
    tomcatcheck=tomcatlib.soft_md5
    maker.inventory_maker(iplist)
    allevent.evt_java_install(version=javaversion,prefix=javaprefix,checksum=javacheck)
    allevent.evt_tomcat_install(version=tomcatversion,prefix=tomcatprefix,checksum=tomcatcheck)
    maker.inventory_clear()

'''
PARM:info for install mysql
RETURN:执行结果
USE:
'''
def batch9mysqlinstall(iplist,mysqlversion,mysqlprefix,mysqlpasswd,mysqldatadir,mysqlport,mysqltmp):
    mysqllib=Softlib.objects.get(id=mysqlversion)
    mysqlversion=mysqllib.soft_version
    mysqlcheck=mysqllib.soft_md5
    print(mysqlversion)
    maker.inventory_maker(iplist)
    allevent.evt_mysql_install(version=mysqlversion,prefix=mysqlprefix,checksum=mysqlcheck,mysqlpasswd=mysqlpasswd,mysqldatadir=mysqldatadir,mysqlport=mysqlport,mysqltmp=mysqltmp)
    maker.inventory_clear()

'''
PARM:info for install redis
RETURN:执行结果
USE:
'''
def batch9redisinstall(iplist,redisversion,redisprefix,redisport,redispasswd):
    redislib=Softlib.objects.get(id=redisversion)
    redisversion=redislib.soft_version
    redischeck=redislib.soft_md5
    maker.inventory_maker(iplist)
    allevent.evt_redis_install(version=redisversion,prefix=redisprefix,checksum=redischeck,port=redisport,requirepass=redispasswd,)
    maker.inventory_clear()

