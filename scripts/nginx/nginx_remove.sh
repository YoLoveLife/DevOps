#!/bin/bash
#Time 2017-1-13 15:36
#Author Yo
PATH=/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
PREFIX=/usr/local
BASEDIR=${PREFIX}/nginx
USER="nginx"
function Help()
{
cat <<_ACEOF
configure nginx_remove bash script.
Usage $0 [OPTION]... [VAR=VALUE]...
	--help	display this help and exit
        -f,--prefix     modify the prefix.Default /usr/local
        -u,--user       modify the user of nginx.Default nginx
_ACEOF
}
function Avrg()
{
	ARGS=`getopt -o f:u: --long prefix:,user: -n 'nginx_remove.sh' -- "$@"`
	if [ ! $? -eq 0 ];then
		echo "001002002"
		exit 2
	fi
	eval set -- "${ARGS}"

	while true
	do
		case "$1" in
			-f|--prefix)
				PREFIX=$2
				shift 2
				;;
			-u|--user)
				USER=$2
				shift 2
				;;
			--)
				shift
				break
				;;
			*)
				#Help
				echo "001002002"
				exit 2	
			esac
	done
}
if [ "$1" == "--help" ];then
	Help
	exit 2
fi
Avrg $@
DIRNAME=${PREFIX}/nginx
rm -rf ${DIRNAME}
if [ "`cat /etc/passwd|grep ${USER}|wc -l`" == "1" ];then
	userdel -r ${USER}
fi
if [ "$?" == "0" ];then
	echo "001000000"
fi
