#!/bin/bash
#Time 2017-02-06 09:23
#Author Yo
#Control redis
source /etc/profile
COMMDDIR=/usr/local/tomcat/bin
function Help()
{
cat <<_ACEOF
control tomcat bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
        help            display this help and exit
        start           start tomcat
        stop            stop tomcat
_ACEOF
}
function Start()
{
    if [ `ps aux |grep java |wc -l` -eq 2 ];then
        echo mysql_online
        exit 2
    fi
    nohup ${COMMDDIR}/catalina.sh start &
}

function Stop()
{
    if [ `ps aux |grep java |wc -l` -eq 1 ];then
        echo mysql_ofline
        exit 2
    fi
    ${COMMDDIR}/catalina.sh stop
}

case "$1" in
    "start")
        Start
        ;;
    "stop")
        Stop
        ;;
        *)
        Help
        ;;
esac