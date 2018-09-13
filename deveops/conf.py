# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-17
# Author Yo
# Email YoLoveLife@outlook.com

# 环境参数 识别运行环境是开发/生产/测试
ENVIRONMENT = 'DEVEL'

# 运行用户
RUN_USER = 'root'

# 数据库配置内容
DB_NAME = 'deveops'
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
REDIS_PASSWD = ''

# 相关目录配置
MEDIA_ROOT = '/media'
OPS_ROOT = '/ops'
WORK_ROOT = '/work'
DASHBOARD_ROOT = '/dashboard'
QCODE_ROOT = '/qrcode'
TOOL_ROOT = '/tool'

# LDAP配置
LDAP_SERVER = ""
LDAP_PASSWD = ""
LDAP_OU = ''

# VMWARE配置
VMWARE_USERNAME = ""
VMWARE_PASSWD = ""
VMWARE_SERVER = ""

# ALiyun配置
ALIYUN_ACCESSKEY = ""
ALIYUN_ACCESSSECRET = ""
ALIYUN_PAGESIZE = 30
ALIYUN_EXPIREDTIME = 13
ALIYUN_OVERDUETIME = -13

# QiNiu配置
QINIU_ACCESSKEY = ""
QINIU_ACCESSSECRET = ""

# 巡检界限
DISK_LIMIT = 10 # %
UPTIME_LIMIT = 70 # %


# SMTP配置
SMTP_HOST = ''
SMTP_PORT = 25
SMTP_USER = ''
SMTP_PASSWD = ''

# DNS服务器
INNER_DNS = ''
OUTER_DNS = ''

# Crontab 配置
from celery.schedules import crontab
DASHBOARD_TIME = crontab(minute=30,hour=1,day_of_week="sunday")
EXPIRED_TIME = crontab(minute=30,hour=1,day_of_week="sunday")
CHECK_TIME = crontab(minute='*')#,day_of_week="sunday")
MANAGER_TIME = crontab(minute=16,hour=10)#,day_of_week="sunday")
DNS_TIME = crontab(minute='*')#,day_of_week="sunday")
