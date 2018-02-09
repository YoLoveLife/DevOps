# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-17
# Author Yo
# Email YoLoveLife@outlook.com

#环境参数 识别运行环境是开发/生产/测试
ENVIRONMENT = 'DEVEL'

#RSA_KEY 默认在当前运行账户下寻找私钥
RSA_KEY = '~/.ssh/id_rsa'

#数据库配置内容
DB_NAME = 'deveops'
DB_USER = 'root'
DB_PASSWD = ''
DB_HOST = '127.0.0.1'
DB_PORT = '3306'

#Session配置
SESSION_COOKIE_AGE = 30*60

#SSH配置
SSH_TIMEOUT = 5

#Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

#相关目录配置
UPLOAD_ROOT = '/devEops/upload'
MEDIA_ROOT = '/devEops/media'
WORK_ROOT = '/devEops/workspace'