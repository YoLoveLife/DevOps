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
from executor.base import shellpb
from inventory import maker
'''
    info:基础配置 包含gcc make libio libselinux except
'''
def evt_base_install():
    basepb.base_personplaybook()

'''
    info:mysql的初次安装 mysql的配置修改 mysql的重启等
'''
def evt_mysql_install(version='10.1.12',prefix='/usr/local',checksum='30a86202c8fe30ad3548988a7ddbf5a3',mysqlpasswd='',mysqlport="3306",mysqltmp='/tmp/mysql.sock',mysqldatadir='/usr/local/mysql/data'):
    mysqlpb.mysql_installplaybook(version=version,prefix=prefix,checksum=checksum,datadir=mysqldatadir)
    #mysqlpb.mysql_configureplaybook(socket=mysqltmp,port=mysqlport)
    mysqlpb.mysql_controlplaybook(control='start')
    mysqlpb.mysql_initializationplaybook(mysqlpasswd=mysqlpasswd)

def evt_mysql_reconfigure(prefix='/usr/local',port='3306',socket='/tmp/mysql.sock',datadir='/usr/local/mysql/data',
                            key_buffer_size='256M',table_open_cache='256',sort_buffer_size='1M',read_buffer_size='1M',read_rnd_buffer_size='4M',
                            query_cache_size='16M',thread_cache_size='8',server_id='1',extend=''):
    #mysqlpb.mysql_configureplaybook(port=port,socket=socket,prefix=prefix,datadir=datadir,key_buffer_size=key_buffer_size,table_open_cache=table_open_cache,sort_buffer_size=sort_buffer_size,read_buffer_size=read_buffer_size,read_rnd_buffer_size=read_rnd_buffer_size,query_cache_size=query_cache_size,thread_cache_size=thread_cache_size,server_id=server_id,extend=extend)
    mysqlpb.mysql_controlplaybook(control='restart')

def evt_mysql_control(control='help',):
    mysqlpb.mysql_controlplaybook(control=control)

'''
    info:java安装卸载
'''
def evt_java_install(server='other'):
    javapb.java_installplaybook(server=server)

def evt_java_remove(server='other'):
    javapb.java_removeplaybook(prefix='/usr/local')

'''
    info:nginx的安装 nginx的配置修改 nginx的重启
'''
def evt_nginx_install(version='1.10.1',prefix='/usr/local',checksum='088292d9caf6059ef328aa7dda332e44',
                      workproc='1',pid='logs/nginx.pid',workconn='1024',port='80',servername='localhost',locations='',):

    nginxpb.nginx_installplaybook(version=version,prefix=prefix,checksum=checksum)
    '''
    nginxpb.nginx_configureplaybook(prefix=prefix,workproc=workproc,pid=pid
                                    ,workconn=workconn,port=port,servername=servername,locations=locations)
    '''
    nginxpb.nginx_controlplaybook(control='start',pid=prefix+'/'+pid)

def evt_nginx_reconfigure(prefix='/usr/local',
                      workproc='1',pid='logs/nginx.pid',workconn='1024',port='80',servername='localhost',locations='',):
    '''
    nginxpb.nginx_configureplaybook(prefix=prefix,workproc=workproc,pid=pid
                                    ,workconn=workconn,port=port,servername=servername,locations=locations)
    '''
    nginxpb.nginx_controlplaybook(control=reload,pid=prefix+'/'+pid)

def evt_nginx_control(control='help',pid='/usr/local/nginx/logs/nginx.pid'):
    nginxpb.nginx_controlplaybook(control=control,pid=pid)

'''
    info:java的安装
'''
def evt_java_install(version='7u79',prefix='/usr/local',checksum='9222e097e624800fdd9bfb568169ccad'):
    javapb.java_installplaybook(version=version,prefix=prefix,checksum=checksum)

'''
    info:tomcat的安装
'''
def evt_tomcat_install(version='7.0.72',prefix='/usr/local',java_opts='',checksum='c24bfae15bb9c510451a05582aae634d'):
    tomcatpb.tomcat_installplaybook(version=version,prefix=prefix,java_opts=java_opts,checksum=checksum)
    tomcatpb.tomcat_controlplaybook(control='start')

def evt_tomcat_control(control='help'):
    tomcatpb.tomcat_controlplaybook(control='start')

'''
    info:redis安装 重新配置
'''
def evt_redis_install(version='3.2.4',prefix='/usr/local',checksum='2f8b49e8004fbbfc807ca7f5faeabec8',
                      bind='0.0.0.0',port='6379',appendonly='yes',noonrewrite='no',saveoptions='save 900 300\nsave 30 10\nsave 2000 1',datadir='{{basedir}}/data',requirepass='000000',slaveof='',masterauth='',cluster_enabled='',cluster_config_file='',extend='',):
    redispb.redis_installplaybook(version=version,prefix=prefix,checksum=checksum,)
    '''
    redispb.redis_configureplaybook(version=version,bind=bind,port=port,appendonly=appendonly,noonrewrite=noonrewrite,saveoptions=saveoptions
                                    ,datadir=datadir,requirepass=requirepass,slaveof=slaveof,masterauth=masterauth,cluster_enabled=cluster_enabled,
                                    cluster_config_file=cluster_config_file,extend=extend,)
    '''
    #redispb.redis_controlplaybook(control='start')


def evt_redis_reconfigure(bind='0.0.0.0',port='6379',appendonly='yes',noonrewrite='no',
                          saveoptions='save 900 300\nsave 30 10\nsave 2000 1',datadir='{{basedir}}/data',requirepass='000000',slaveof='',
                          masterauth='',cluster_enabled='',cluster_config_file='',extend='',):
    '''
    redispb.redis_configureplaybook(bind=bind,port=port,appendonly=appendonly,noonrewrite=noonrewrite,saveoptions=saveoptions
                                    ,datadir=datadir,requirepass=requirepass,slaveof=slaveof,masterauth=masterauth,cluster_enabled=cluster_enabled,
                                    cluster_config_file=cluster_config_file,extend=extend,)
    '''
    redispb.redis_controlplaybook(control='stop')
    redispb.redis_controlplaybook(control='start')

def evt_redis_control(control='help',passwd='000000'):
    redispb.redis_controlplaybook(control=control,passwd=passwd)

def evt_redis_remove(prefix='/usr/local'):
    redispb.redis_removeplaybook(prefix=prefix)

def evt_shell_control(control='hostname'):
    shellpb.shell_book(control)


#maker.inventory_maker(['192.168.254.129'])
#evt_redis_remove(server="all",)
#evt_redis_install(server="all",)
