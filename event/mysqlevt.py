# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 08 11:35
# Author Yo
# Email YoLoveLife@outlook.com

from executor.mysql import mysqlpb
def evt_mysql_install(server='other',version='10.1.12',prefix='/usr/local',checksum='',mysqlpasswd=''):
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

if __name__=='__main__':
    evt_mysql_install(server='mysql-server',version='10.1.12',prefix='/usr/local',checksum='30a86202c8fe30ad3548988a7ddbf5a3',mysqlpasswd='000000')
    evt_mysql_reconfigure(server='mysql-server')