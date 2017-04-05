#!/bin/bash
# Author Yo
# Email YoLoveLife@outlook.com
# Time 2017-03-07 09:25
source /etc/profile
COMMDDIR=/usr/local/nginx/sbin
function Help()
{
cat <<_ACEOF
control nginx bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
        help            display this help and exit
        start           start nginx
        stop            stop nginx
        reload          reload nginx conf
        test            test nginx conf.Default nginx conf/nginx.conf
_ACEOF
}
function Start()
{
    if [ -f $2 ];then
        echo nginx_online
        exit 2
    fi
    ${COMMDDIR}/nginx
}
function Stop()
{
    if [ ! -f $2 ];then
        echo nginx_ofline
        exit 2
    fi
    ${COMMDDIR}/nginx -s stop
}
function Test()
{
    ${COMMDDIR}/nginx -t
}
function Reload()
{
    if [ -f $2 ];then
        ${COMMDDIR}/nginx -s reload
    else
        echo nginx_ofline
        exit 2
    fi

}
case "$1" in
    "start")
        Start $@
        ;;
    "stop")
        Stop $@
        ;;
    "test")
        Test
        ;;
    "reload")
        Reload $@
        ;;
    *)
        Help
        ;;
esac