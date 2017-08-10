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
    nohup ${COMMDDIR}/catalina.sh start &
}

function Stop()
{
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
