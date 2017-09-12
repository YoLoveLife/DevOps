# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
import json
ecode={
    '001000000':"Redis安装成功",
    '001001002':"Redis在默认目录已安装",
    '001002002':'Redis安装参数错误',
    '001003002':'Redis安装缺少依赖',
    '001005003':'Redis安装权限错误',
    '001004001':'Redis安装包缺失',
    '001007003':'Redis安装错误',
    '001008002':'Redis配置文件丢失',
    '001006001':'Redis安装环境错误',
    '001009001':'Redis未安装',
    '002000000':'MySQL安装成功',
    '002001002':'MySQL在默认目录已安装',
    '002002002':'MySQL安装参数错误',
    '002004001':'MySQL安装包缺失',
    '002006001':'MySQL安装环境错误',
    '002005002':'MySQL运行中',
    '003004001':'Java安装包丢失',
    '003001002':'Java在默认目录已安装',
    '003002002':'Java安装参数错误',
}
def analyze_ecode(result,):
    host = result._host
    print json.dumps({host.name: result._result}, indent=4)