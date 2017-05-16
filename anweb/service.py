# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17 17:18
# Author Yo
# Email YoLoveLife@outlook.com
from models import Group
from django.core import serializers
from util import toJSON,str2dict
from anweb.models import Group,Host,Softlib,Soft,Redis,MySQL,Tomcat,Java,Nginx,History,State,Operation
from django.forms.models import model_to_dict
from event import allevent
from inventory import maker
import json


'''
PARM:null
RETURN:list
USE:返回对应id的服务器IP
'''
def batch9ID2IP(idlist):
    iplist=[]
    for id in idlist:
        host=Host.objects.get(id=id)
        iplist.append(host.sship)

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
PARM:ipaddress,groupid
RETURN:status
USE:
'''
def host9hostupdate(ipaddress,groupid):
    group=Group.objects.get(id=groupid)
    host=Host(group=group,sship=unicode.encode(ipaddress))
    host.save()
    maker.inventory_maker([ipaddress])
    allevent.evt_base_install()
    maker.inventory_clear()
    historyCreate(2,host.sship,2)
    return 1

'''
PARM:group_id,group_name,group_remark
RETURN:TRUE/FALSE
USE:如果组不存在 则添加组；如果组存在 则修改组
'''
def group9modifygroup(group_id,group_name,group_remark):
    if group_id == "1":#ADD
        group=Group(name=unicode.encode(group_name),remark=unicode.encode(group_remark))
        #print(group_id,group_name,group_remark)
        group.save()
    else:#UPDATE
        Group.objects.filter(id=int(group_id)).update(name=unicode.encode(group_name),remark=unicode.encode(group_remark))
    historyCreate(1,'',2)

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
    list=[]
    for i in iplist:
        tomcat=Tomcat(host_id=int(i),prefix=tomcatprefix,softlib_id=tomcatversion)
        java=Java(host_id=int(i),prefix=javaprefix,softlib_id=javaversion)
        tomcat.save()
        java.save()
        host=Host.objects.get(id=unicode.encode(i))
        list.append(host.sship)
    tomcatlib=Softlib.objects.get(id=tomcatversion)
    javalib=Softlib.objects.get(id=javaversion)
    tomcatversion =tomcatlib.soft_version
    javaversion=javalib.soft_version
    javacheck=javalib.soft_md5
    tomcatcheck=tomcatlib.soft_md5

    history=historyCreate(5,'',1)

    maker.inventory_maker(list)
    allevent.evt_java_install(version=javaversion,prefix=javaprefix,checksum=javacheck)
    allevent.evt_tomcat_install(version=tomcatversion,prefix=tomcatprefix,checksum=tomcatcheck)
    maker.inventory_clear()

    historyUpdate(history,'',2)
'''
PARM:info for install mysql
RETURN:执行结果
USE:
'''
def batch9mysqlinstall(iplist,version,prefix,passwd,datadir,port,socket):
    list=[]
    for i in iplist:
        mysql=MySQL(host_id=int(i),prefix=prefix,passwd=passwd,port=port,socket=socket,datadir=datadir,softlib_id=int(version))
        mysql.save()
        host=Host.objects.get(id=unicode.encode(i))
        list.append(host.sship)
    mysqllib=Softlib.objects.get(id=version)
    mysqlversion=mysqllib.soft_version
    mysqlcheck=mysqllib.soft_md5

    history=historyCreate(6,'',1)

    maker.inventory_maker(list)
    allevent.evt_mysql_install(version=mysqlversion,prefix=prefix,checksum=mysqlcheck,mysqlpasswd=passwd,mysqldatadir=datadir,mysqlport=port,mysqlsocket=socket)
    maker.inventory_clear()

    historyUpdate(history,'',2)

'''
PARM:info for install redis
RETURN:执行结果
USE:
'''
def batch9redisinstall(iplist,redisversion,redisprefix,redisport,redispasswd,redisdatadir):
    list=[]
    for i in iplist:
        redis = Redis(host_id=int(i),prefix=redisprefix,port=redisport,requirepass=redispasswd,datadir=redisdatadir,softlib_id=int(redisversion))
        redis.save()
        host=Host.objects.get(id=unicode.encode(i))
        list.append(host.sship)
    redislib=Softlib.objects.get(id=redisversion)
    redisversion=redislib.soft_version
    redischeck=redislib.soft_md5

    history=historyCreate(3,'',1)

    maker.inventory_maker(list)
    allevent.evt_redis_install(version=redisversion,prefix=redisprefix,checksum=redischeck,datadir=redisdatadir)
    maker.inventory_clear()

    historyUpdate(history,'',2)

'''
PARM: info for install nginx
RETURN:执行结果
USE:
'''
def batch9nginxinstall(iplist,version,prefix,pid):
    list=[]
    for i in iplist:
        nginx=Nginx(host_id=int(i),prefix=prefix,pid=pid,softlib_id=int(version))
        nginx.save()
        host=Host.objects.get(id=unicode.encode(i))
        list.append(host.sship)
    nginxlib=Softlib.objects.get(id=version)
    nginxversion=nginxlib.soft_version
    nginxcheck=nginxlib.soft_md5

    history=historyCreate(4,'',1)
    maker.inventory_maker(list)
    allevent.evt_nginx_install(version=nginxversion,prefix=prefix,checksum=nginxcheck)
    maker.inventory_clear()

    historyUpdate(history,'',2)

'''
PARM:
RETURN:history
USE:
'''
def historyCreate(type,hostlist,result):
    history=History(oper_type_id=type,oper_hostlist=hostlist,oper_info='',oper_result_id=result)
    history.save()
    return history

'''
PARM:
RETURN:NULL
USE:
'''
def historyUpdate(history,info,result):
    history.oper_info=info
    history.oper_result_id=result
    history.save()

def historyget():
    a = History.objects.all()
    list=[]
    for history in a:
        tmpdict=model_to_dict(history)
        tmpdict['oper_time']=history.oper_time.strftime('%Y-%m-%d %H:%M')
        list.append(json.dumps(tmpdict))
    return list

def cnfget(iplist,cnf):
    list=[]
    for i in iplist:
        host=Host.objects.get(id=unicode.encode(i))
        list.append(host.sship)

    maker.inventory_maker(list)
    str=allevent.evt_dispatch_getcnf(cnf)
    maker.inventory_clear()
    return str

def cnfmodify(iplist,tmp,newstr,cnf):
    list=[]
    for i in iplist:
        host=Host.objects.get(id=unicode.encode(i))
        list.append(host.sship)

    history=historyCreate(8,'',1)

    maker.inventory_maker(list)
    str=allevent.evt_dispatch_setcnf(newstr,tmp,cnf)
    maker.inventory_clear()

    historyUpdate(history,'',2)

def applist(appname):
    list = []
    a=[]
    if appname=="redis":
        a=Redis.objects.all()
    elif appname=="nginx":
        a=Nginx.objects.all()
    elif appname=="mysql":
        a=MySQL.objects.all()
    elif appname=="tomcat":
        a=Tomcat.objects.all()
    for app in a:
        tmpdict = model_to_dict(app)
        host=Host.objects.get(id=int(tmpdict['host']))
        group=Group.objects.get(id=int(host.group_id))
        tmpdict['hostname']=host.name
        tmpdict['groupname']=group.name
        list.append(json.dumps(tmpdict))
    return list

def appcontrol(hostid,type,appname):
    list=[]
    host=Host.objects.get(id=hostid)
    list.append(host.sship)
    history=historyCreate(9,host.sship,1)
    maker.inventory_maker(list)
    if appname=='redis':
        redis=Redis.objects.get(host_id=int(hostid))
        allevent.evt_redis_control(control=type,passwd=redis.requirepass)
        if type=='stop':
            redis.online=False
        else:
            redis.online=True
        redis.save()
    elif appname=='tomcat':
        tomcat=Tomcat.objects.get(host_id=int(hostid))
        allevent.evt_tomcat_control(control=type)
        if type=='stop':
            tomcat.online=False
        else:
            tomcat.online=True
        tomcat.save()
    elif appname=='mysql':
        mysql=MySQL.objects.get(host_id=int(hostid))
        allevent.evt_mysql_control(control=type)
        if type=='stop':
            mysql.online=False
        else:
            mysql.online=True
        mysql.save()
    elif appname=='nginx':
        nginx=Nginx.objects.get(host_id=int(hostid))
        allevent.evt_nginx_control(control=type,pid=nginx.pid)
        if type=='stop':
            nginx.online=False
        else:
            nginx.online=True
        nginx.save()
    maker.inventory_clear()
    historyUpdate(history,host.sship,2)

def appremove(hostid,appname):
    list=[]
    host=Host.objects.get(id=hostid)
    list.append(host.sship)
    history=historyCreate(9,host.sship,1)
    maker.inventory_maker(list)
    if appname=='redis':
        redis=Redis.objects.get(host_id=int(hostid))
        allevent.evt_redis_remove(prefix=redis.prefix)
    elif appname=='mysql':
        mysql=MySQL.objects.get(host_id=int(hostid))
        allevent.evt_mysql_remove(prefix=mysql.prefix,datadir=mysql.datadir)
    elif appname=='nginx':
        nginx=Nginx.objects.get(host_id=int(hostid))
        allevent.evt_nginx_remove(prefix=nginx.prefix,)
    elif appname=='tomcat':
        tomcat=Tomcat.objects.get(host_id=int(hostid))
        allevent.evt_tomcat_remove(prefix=tomcat.prefix)
    elif appname=='java':
        java=Java.objects.get(host_id=int(hostid))
        allevent.evt_java_remove(prefix=java.prefix)

    maker.inventory_clear()
    historyUpdate(history,host.sship,2)
