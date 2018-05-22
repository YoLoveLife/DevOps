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
REDIS_PORT = 6379
REDIS_SPACE = 3

# 相关目录配置
MEDIA_ROOT = '/media/'
OPS_ROOT = '/ops/'

# LDAP配置
LDAP_SERVER = "ldap://10.100.61.6:389"
LDAP_PASSWD = "7a$LIOOwxNO"
LDAP_OU = 'ou=集团所属公司,ou=浙报集团,dc=zbjt,dc=com'

# VMWARE配置
VMWARE_USERNAME = "zbjt\yz2"
VMWARE_PASSWD = "daiSgmiku2"
VMWARE_SERVER = "10.100.60.110"

# ALiyun配置
ALIYUN_ACCESSKEY = "LTAIdXTBaAPhuqB7"
ALIYUN_ACCESSSECRET = "e0LH3BJLSjFV4MiXsRmS4IScgtAhwE"
ALIYUN_PAGESIZE = 10
EXPIREDTIME = 10