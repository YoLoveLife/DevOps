# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 08 11:35
# Author Yo
# Email YoLoveLife@outlook.com
from executor.base import basepb
from executor.mysql import mysqlpb
from executor.java import javapb
from executor.nginx import nginxpb
from executor.tomcat import tomcatpb
from executor.redis import redispb
'''
    info:基础配置 包含gcc make libio libselinux except
'''
def evt_base_install(server='other'):
    basepb.base_personplaybook(server=server)

'''
    info:mysql的初次安装 mysql的配置修改 mysql的重启等
'''
def evt_mysql_install(server='other',version='10.1.12',prefix='/usr/local',checksum='30a86202c8fe30ad3548988a7ddbf5a3',mysqlpasswd=''):
    mysqlpb.mysql_installplaybook(server=server,version=version,prefix=prefix,checksum=checksum)
    mysqlpb.mysql_controlplaybook(server=server,control='start')
    mysqlpb.mysql_configureplaybook(server=server,)
    mysqlpb.mysql_initializationplaybook(server=server,mysqlpasswd=mysqlpasswd)

def evt_mysql_reconfigure(server='other',prefix='/usr/local',port='3306',socket='/tmp/mysql.sock',datadir='/usr/local/mysql/data',
                            key_buffer_size='256M',table_open_cache='256',sort_buffer_size='1M',read_buffer_size='1M',read_rnd_buffer_size='4M',
                            query_cache_size='16M',thread_cache_size='8',server_id='1',extend=''):
    mysqlpb.mysql_configureplaybook(server=server,port=port,socket=socket,prefix=prefix,datadir=datadir,key_buffer_size=key_buffer_size,table_open_cache=table_open_cache,sort_buffer_size=sort_buffer_size,read_buffer_size=read_buffer_size,read_rnd_buffer_size=read_rnd_buffer_size,query_cache_size=query_cache_size,thread_cache_size=thread_cache_size,server_id=server_id,extend=extend)
    mysqlpb.mysql_controlplaybook(server=server,control='restart')

def evt_mysql_control(server='other',control='help',):
    mysqlpb.mysql_controlplaybook(server=server,control=control)

'''
    info:java安装卸载
'''
def evt_java_install():
    javapb.java_installplaybook(server='tomcat-server')

def evt_java_remove():
    javapb.java_removeplaybook(server='tomcat-server',prefix='/usr/local')

'''
    info:nginx的安装 nginx的配置修改 nginx的重启
'''
def evt_nginx_install(server='other',version='1.10.1',prefix='/usr/local',checksum='088292d9caf6059ef328aa7dda332e44',
                      workproc='1',pid='logs/nginx.pid',workconn='1024',port='80',servername='localhost',locations='',):

    nginxpb.nginx_installplaybook(server=server,version=version,prefix=prefix,checksum=checksum)
    nginxpb.nginx_configureplaybook(server=server,prefix=prefix,workproc=workproc,pid=pid
                                    ,workconn=workconn,port=port,servername=servername,locations=locations)
    nginxpb.nginx_controlplaybook(server=server,control='start',pid=prefix+'/'+pid)

def evt_nginx_reconfigure(server='other',prefix='/usr/local',
                      workproc='1',pid='logs/nginx.pid',workconn='1024',port='80',servername='localhost',locations='',):
    nginxpb.nginx_configureplaybook(server=server,prefix=prefix,workproc=workproc,pid=pid
                                    ,workconn=workconn,port=port,servername=servername,locations=locations)
    nginxpb.nginx_controlplaybook(server=server,control=reload,pid=prefix+'/'+pid)

def evt_nginx_control(server='other',control='help',pid='/usr/local/nginx/logs/nginx.pid'):

    nginxpb.nginx_controlplaybook(server=server,control=control,pid=pid)

'''
    info:tomcat的安装
'''
def evt_tomcat_install(server='other',version='7.0.72',prefix='/usr/local',java_opts='',checksum='c24bfae15bb9c510451a05582aae634d'):
    tomcatpb.tomcat_installplaybook(server==server,version=version,prefix=prefix,java_opts=java_opts,checksum=checksum)
    tomcatpb.tomcat_controlplaybook(server=server,control='start')

def evt_tomcat_control(server='other',control='help'):
    tomcatpb.tomcat_controlplaybook(server=server,control=control)

'''
    info:redis安装 重新配置
'''
def evt_redis_install(server='other',version='3.2.4',prefix='/usr/local',checksum='2f8b49e8004fbbfc807ca7f5faeabec8',
                      bind='0.0.0.0',port='6379',appendonly='yes',noonrewrite='no',saveoptions='save 900 300\nsave 30 10\nsave 2000 1',datadir='{{basedir}}/data',requirepass='000000',slaveof='',masterauth='',cluster_enabled='',cluster_config_file='',extend='',):
    redispb.redis_installplaybook(server=server,version=version,prefix=prefix,checksum=checksum,
    )
    redispb.redis_configureplaybook(server=server,bind=bind,port=port,appendonly=appendonly,noonrewrite=noonrewrite,saveoptions=saveoptions
                                    ,datadir=datadir,requirepass=requirepass,slaveof=slaveof,masterauth=masterauth,cluster_enabled=cluster_enabled,
                                    cluster_config_file=cluster_config_file,extend=extend,)
    redispb.redis_controlplaybook(server=server,control='start')

def evt_redis_reconfigure(server='other',bind='0.0.0.0',port='6379',appendonly='yes',noonrewrite='no',
                          saveoptions='save 900 300\nsave 30 10\nsave 2000 1',datadir='{{basedir}}/data',requirepass='000000',slaveof='',
                          masterauth='',cluster_enabled='',cluster_config_file='',extend='',):
    redispb.redis_configureplaybook(server=server,bind=bind,port=port,appendonly=appendonly,noonrewrite=noonrewrite,saveoptions=saveoptions
                                    ,datadir=datadir,requirepass=requirepass,slaveof=slaveof,masterauth=masterauth,cluster_enabled=cluster_enabled,
                                    cluster_config_file=cluster_config_file,extend=extend,)
    redispb.redis_controlplaybook(server=server,control='stop')
    redispb.redis_controlplaybook(server=server,control='start')

def evt_redis_control(server='other',control='help'):
    redispb.redis_controlplaybook(server='redis-server',control=control)

