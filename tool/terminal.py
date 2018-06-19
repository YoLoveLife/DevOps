# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-19
# Author Yo
# Email YoLoveLife@outlook.com

# ENV
import termios, tty, sys, os, django
sys.path.append("/code/dev/deveops")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

#PREPARE
status = 0
# STATUS 0未登陆 1已登陆 2打印应用组 3打印主机 4建立连接
import getpass
username = getpass.getuser()
from authority.models import ExtendUser
if ExtendUser.objects.filter(username=username).exists():
    user = ExtendUser.objects.filter(username=username).get()
    print(user.full_name+'已成功登陆devEops平台跳板机')
else:
    print('当前用户不存在devEops平台当中 请通知管理员')
    exit(0)

verifycode=input('请输入qrcode：')
print(user.check_qrcode(verifycode))




# INPUT
tty_fd = sys.stdin.fileno()
tty_old_settings = termios.tcgetattr(tty_fd)
BUFFER = []
tty.setraw(sys.stdin.fileno())


def ddr():
    ch = sys.stdin.read(1)
    return ch

while True:
    ch = ddr()
    if ch != '\n':
        # sys.stdout.flush()
        BUFFER.append(ch)
    elif ''.join(BUFFER) == 'exit':
        break
    else:
        print('需要处理的数据',''.join(BUFFER))
        BUFFER = []
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, tty_old_settings)