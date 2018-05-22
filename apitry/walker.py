# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-2-27
# Author Yo
# Email YoLoveLife@outlook.com
import os,shutil
def move_file(src_file,dest_file):
    shutil.move(src=src_file,dst=dest_file)#Move

def walker(dir):
    file_list = []
    for dirpath,dirname,filename in os.walk(dir):
        for dir in dirname:
            file_list.append(os.path.join(dirpath,dir))
        for name in filename:
            file_list.append(os.path.join(dirpath,name))
    return file_list


if __name__ == '__main__':
    print(walker('/tmp/'))