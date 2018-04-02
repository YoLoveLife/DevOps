# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-17
# Author Yo
# Email YoLoveLife@outlook.com

#环境参数 识别运行环境是开发/生产/测试
ENVIRONMENT = 'DEVEL'

# 运行用户
RUN_USER = 'root'

# 数据库配置内容
DB_NAME = 'deveops_dev'
DB_USER = 'root'
DB_PASSWD = ''
DB_HOST = '127.0.0.1'
DB_PORT = '3306'

# Session配置
SESSION_COOKIE_AGE = 30*60

# SSH配置
SSH_TIMEOUT = 2

# Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6389

# 相关目录配置
UPLOAD_ROOT = '/devEops/upload'
MEDIA_ROOT = '/devEops/media'
WORK_ROOT = '/devEops/workspace'

# LDAP配置
LDAP_SERVER = "ldap://0.0.0.0:389"
LDAP_PASSWD = ""
LDAP_OU = unicode('ou=,ou=,dc=,dc=com','utf8')

# VMWARE配置
VMWARE_USERNAME = ""
VMWARE_PASSWD = ""
VMWARE_SERVER = ""

# ALiyun配置
ALIYUN_ACCESSKEY = ""
ALIYUN_ACCESSSECRET = ""