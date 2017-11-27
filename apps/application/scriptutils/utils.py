# -*- coding:utf-8 -*-
import constant
import re

def bash_writer(*args,**kwargs):
    return bash_head(*args,**kwargs)

def bash_head(author,time,*args,**kwargs):#author time
    string = "#!/bin/bash" + "\n"
    string = string + "# Author "+ author + "\n"

    string += "# Time " + time + "\n"

    return string + args_maker(*args,**kwargs)

# def args_maker(*args,**kwargs):
#     string = ""
#     OPTIONS = ""
#     CASE_ITEMS = ""
#     for key in kwargs:
#         if kwargs[key] == "1":
#             OPTIONS += key+':'
#             CASE_ITEMS += constant.EXTEND_CASE_ITEM%(key,key)
#         else:
#             OPTIONS += key
#             CASE_ITEMS += constant.SIMPLE_CASE_ITEM%(key,key)
#         OPTIONS += ','
#     command = 'ARGS=`getopt -o y --long %s -- "$@"`'%(OPTIONS)
#     string = string + constant.FUNCTION_ARGS%(command,CASE_ITEMS+constant.CASE_END)
#     string = string + 'Args $@\n'
#     return string
def args_maker( *args, **kwargs):
    string = ""
    for key in kwargs:
        string += key + '=' + kwargs[key] +'\n'
    return string

def html2bash(str):#去除HTML p选项
    result , number = re.subn(constant.PATTERN_BR,'\n',str)
    result , number = re.subn(constant.PATTERN_P,'\n',result)
    result , number = re.subn(constant.PATTERN_F_P, '\n', result)
    return result

if __name__ == "__main__":
    kwargs={}
    print(bash_writer(author='Yo',time='2017-8-11 16:44:13',**kwargs))
    string = "<p>hostname<br>cat /proc/cpuinfo |grep processor|wc -l<br>free -m|sed -n '2p' |awk '{ print $2 }'<br>df -h |grep '/$' |awk '{ print $2 }'</p>"
    print(html2bash(string))