# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-16
# Author Yo
# Email YoLoveLife@outlook.com

def decorator_manager(asset_id,api_name,):#host group storage
    def wrapper(func):
        def inner_wrapper():
            print(name)
            func()
        return inner_wrapper
    return wrapper

@decorator_host(name='ddr')
def ddr():
    print('function')

if __name__ == '__main__':
    ddr()