# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-24
# Author Yo
# Email YoLoveLife@outlook.com

import re
def checkLen(passwd):
    return len(passwd)>12

def checkContainUpper(passwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(passwd)
    if match:
        return True
    else:
        return False

def checkContainNum(passwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(passwd)
    if match:
        return True
    else:
        return False

def checkContainLower(passwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(passwd)
    if match:
        return True
    else:
        return False

def checkSymbol(passwd):
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(passwd)
    if match:
        return True
    else:
        return False

def checkPassword(passwd):
    # lenOK = checkLen(passwd)
    upperOK = checkContainUpper(passwd)
    lowerOK = checkContainLower(passwd)
    # numOK = checkContainNum(passwd)
    # symbolOK = checkSymbol(passwd)
    # return (lenOK and upperOK and lowerOK and numOK and symbolOK)
    return (upperOK and lowerOK)