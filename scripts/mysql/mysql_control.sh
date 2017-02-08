#!/bin/bash
#Time 2017-02-06 09:23
#Author Yo
#Control redis
COMMDDIR=/etc/init.d
function Help()
{
cat <<_ACEOF
control mysql bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
        help            display this help and exit
        start           start mysql with /etc/my.cnf
        stop            stop mysql
        restart         restart mysql
_ACEOF
}
function Start()
{
    if [ `ps aux |grep mysql |wc -l` -eq 3 ];then
        echo mysql_online
        exit 2
    fi
    ${COMMDDIR}/mysqld start
}

function Stop()
{
    if [ `netstat -tln |grep 3306 |wc -l` -eq 0 ];then
        echo mysql_ofline
        exit 2
    fi
    ${COMMDDIR}/mysqld stop
}

function Restart()
{
    Stop
    Start
}

case "$1" in
    "start")
        Start
        ;;
    "stop")
        Stop
        ;;
    "restart")
        Restart
        ;;
        *)
        Help
        ;;
esac